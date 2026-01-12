"""
Simple chat API using Google Gemini (free API).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
import google.generativeai as genai

from src.database import get_db
from src.auth.middleware import get_current_user
from src.models.user import User
from src.models.chat import Conversation, ChatMessage
from src.config import settings
from sqlalchemy import select

router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str


def get_gemini_client():
    """Initialize and return Gemini client."""
    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "":
        raise HTTPException(
            status_code=503,
            detail="Google API key not configured. Please set GOOGLE_API_KEY in .env file. Get free key at: https://aistudio.google.com/app/apikey"
        )

    genai.configure(api_key=settings.GOOGLE_API_KEY)
    return genai.GenerativeModel('gemini-pro')


async def get_task_context(db: AsyncSession, user_id: UUID) -> str:
    """Get current tasks for context."""
    from src.models.task import Task
    result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )
    tasks = result.scalars().all()

    if not tasks:
        return "User has no tasks yet."

    task_list = []
    for task in tasks:
        status = "✓ Completed" if task.is_completed else "○ Pending"
        task_list.append(f"- {status}: {task.title}" + (f" ({task.description})" if task.description else ""))

    return "Current tasks:\n" + "\n".join(task_list)


async def execute_task_operation(
    db: AsyncSession,
    user_id: UUID,
    operation: str,
    task_title: Optional[str] = None,
    task_description: Optional[str] = None,
    task_id: Optional[UUID] = None
) -> str:
    """Execute task CRUD operations."""
    from src.models.task import Task

    if operation == "add" and task_title:
        new_task = Task(
            user_id=user_id,
            title=task_title,
            description=task_description or "",
            is_completed=False
        )
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return f"✓ Task added: '{task_title}'"

    elif operation == "list":
        return await get_task_context(db, user_id)

    elif operation == "complete" and task_title:
        result = await db.execute(
            select(Task).where(
                Task.user_id == user_id,
                Task.title.ilike(f"%{task_title}%"),
                Task.is_completed == False
            )
        )
        task = result.scalar_one_or_none()

        if task:
            task.is_completed = True
            await db.commit()
            return f"✓ Completed: '{task.title}'"
        return f"✗ No pending task found matching '{task_title}'"

    elif operation == "delete" and task_title:
        result = await db.execute(
            select(Task).where(
                Task.user_id == user_id,
                Task.title.ilike(f"%{task_title}%")
            )
        )
        task = result.scalar_one_or_none()

        if task:
            title = task.title
            await db.delete(task)
            await db.commit()
            return f"✓ Deleted: '{title}'"
        return f"✗ No task found matching '{task_title}'"

    return "✗ Invalid operation"


def parse_user_intent(message: str) -> tuple[str, Optional[str], Optional[str]]:
    """Parse user message to extract intent and task details."""
    message_lower = message.lower()

    # Add task
    if any(word in message_lower for word in ['add', 'create', 'new task', 'remind me']):
        # Extract task title
        for prefix in ['add task', 'add a task', 'create task', 'new task', 'remind me to', 'add']:
            if prefix in message_lower:
                task_title = message[message_lower.index(prefix) + len(prefix):].strip()
                task_title = task_title.lstrip('to ').strip()
                if task_title:
                    return ('add', task_title, None)
        return ('add', None, None)

    # List tasks
    if any(word in message_lower for word in ['list', 'show', 'what tasks', 'my tasks', 'todo']):
        return ('list', None, None)

    # Complete task
    if any(word in message_lower for word in ['complete', 'done', 'finish', 'mark as complete']):
        for prefix in ['complete', 'done with', 'finished', 'mark as complete']:
            if prefix in message_lower:
                task_title = message[message_lower.index(prefix) + len(prefix):].strip()
                task_title = task_title.lstrip('the ').lstrip('task ').strip()
                if task_title:
                    return ('complete', task_title, None)
        return ('complete', None, None)

    # Delete task
    if any(word in message_lower for word in ['delete', 'remove', 'cancel']):
        for prefix in ['delete', 'remove', 'cancel']:
            if prefix in message_lower:
                task_title = message[message_lower.index(prefix) + len(prefix):].strip()
                task_title = task_title.lstrip('the ').lstrip('task ').strip()
                if task_title:
                    return ('delete', task_title, None)
        return ('delete', None, None)

    return ('chat', None, None)


@router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Simple chat endpoint using Google Gemini.
    Handles natural language task management.
    """

    # Get or create conversation
    conversation_id = None
    if request.conversation_id:
        try:
            conversation_id = UUID(request.conversation_id)
            result = await db.execute(
                select(Conversation).where(
                    Conversation.conversation_id == conversation_id,
                    Conversation.user_id == current_user.user_id
                )
            )
            conv = result.scalar_one_or_none()
            if not conv:
                conv = Conversation(user_id=current_user.user_id)
                db.add(conv)
                await db.commit()
                await db.refresh(conv)
                conversation_id = conv.conversation_id
        except:
            conv = Conversation(user_id=current_user.user_id)
            db.add(conv)
            await db.commit()
            await db.refresh(conv)
            conversation_id = conv.conversation_id
    else:
        conv = Conversation(user_id=current_user.user_id)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        conversation_id = conv.conversation_id

    # Save user message
    user_msg = ChatMessage(
        conversation_id=conversation_id,
        role="user",
        content=request.message
    )
    db.add(user_msg)
    await db.commit()

    # Parse intent and execute task operations
    operation, task_title, task_desc = parse_user_intent(request.message)

    response_text = ""

    if operation in ['add', 'list', 'complete', 'delete']:
        # Execute task operation
        operation_result = await execute_task_operation(
            db, current_user.user_id, operation, task_title, task_desc
        )
        response_text = operation_result
    else:
        # Use Gemini for general chat
        try:
            model = get_gemini_client()
            task_context = await get_task_context(db, current_user.user_id)

            system_prompt = f"""You are a helpful todo assistant. Help the user manage their tasks.

{task_context}

Instructions:
- Be friendly and concise
- For task operations, guide users to use commands like: "add task [name]", "list tasks", "complete [task]", "delete [task]"
- Don't make up or assume task information
"""

            full_prompt = f"{system_prompt}\n\nUser: {request.message}\nAssistant:"
            response = model.generate_content(full_prompt)
            response_text = response.text
        except Exception as e:
            response_text = f"I'm here to help! Try: 'add task [name]', 'list tasks', 'complete [task]', or 'delete [task]'"

    # Save assistant response
    assistant_msg = ChatMessage(
        conversation_id=conversation_id,
        role="assistant",
        content=response_text
    )
    db.add(assistant_msg)
    await db.commit()

    return ChatResponse(
        conversation_id=str(conversation_id),
        response=response_text
    )
