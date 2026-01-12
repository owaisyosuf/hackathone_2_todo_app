"""
Chat API endpoints for conversational AI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import uuid

from src.database import get_db
from src.auth.middleware import get_current_user
from src.models.user import User
from src.models.chat import Conversation, ChatMessage
from src.agents.todo_agent import get_todo_agent
from src.db.repository import get_conversation_history, create_chat_message
from agents import Runner, Message

router = APIRouter(tags=["Chat"])

@router.post("/chat")
async def chat_with_ai(
    message: str,
    conversation_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Direct chat endpoint with the AI agent.
    - Persists messages in DB.
    - Loads up to 30 messages of history for context.
    - Executes Agent with MCP tools.
    """

    # 1. Resolve or create conversation
    if conversation_id:
        from sqlalchemy import select
        res = await db.execute(select(Conversation).where(
            Conversation.conversation_id == conversation_id,
            Conversation.user_id == current_user.user_id
        ))
        conv = res.scalar_one_or_none()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = Conversation(user_id=current_user.user_id)
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        conversation_id = conv.conversation_id

    # 2. Persist user message
    await create_chat_message(db, conversation_id, "user", message)

    # 3. Load history for context (last 30 messages for US2)
    history = await get_conversation_history(db, conversation_id, current_user.user_id, limit=30)

    # Map to Agent Message format
    agent_messages = [
        Message(role=msg.role, content=msg.content)
        for msg in history
    ]

    # 4. Get Agent and Run
    agent = get_todo_agent(str(current_user.user_id))

    # Note: agents SDK Runner.run is async and handles the loop
    # For US1/US2, we use standard tool execution within the runner context
    result = await Runner.run(agent, agent_messages)

    # 5. Persist assistant response
    assistant_content = result.final_message if hasattr(result, 'final_message') else str(result)
    await create_chat_message(db, conversation_id, "assistant", assistant_content)

    return {
        "conversation_id": conversation_id,
        "response": assistant_content,
        "history": [msg.content for msg in history] + [assistant_content]
    }
