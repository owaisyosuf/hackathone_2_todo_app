"""
Chat API endpoints for conversational AI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import uuid
import time
import jwt

from src.database import get_db
from src.auth.middleware import get_current_user
from src.models.user import User
from src.models.chat import Conversation, ChatMessage
from src.agents.todo_agent import get_todo_agent
from src.db.repository import get_conversation_history, create_chat_message
from src.config import settings
from agents import Runner

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

    # Map to Agent input format - convert history to conversation messages
    # For openai-agents 0.6.x, we need to pass the conversation as a list of dicts
    agent_messages = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]

    # 4. Get Agent and Run
    agent = get_todo_agent(str(current_user.user_id))

    # Note: agents SDK Runner.run_sync is async and handles the loop
    # For US1/US2, we use standard tool execution within the runner context
    result = await Runner.run_sync(agent, agent_messages)

    # 5. Persist assistant response
    # Extract the final response from the runner result
    assistant_content = ""
    if hasattr(result, 'messages') and len(result.messages) > 0:
        last_msg = result.messages[-1]
        assistant_content = last_msg.get('content', str(result))
    elif hasattr(result, 'content'):
        assistant_content = result.content
    else:
        assistant_content = str(result)
    await create_chat_message(db, conversation_id, "assistant", assistant_content)

    return {
        "conversation_id": conversation_id,
        "response": assistant_content,
        "history": [msg.content for msg in history] + [assistant_content]
    }


@router.post("/session")
async def create_chatkit_session(
    current_user: User = Depends(get_current_user)
):
    """
    Create a ChatKit session and return a client secret.

    OpenAI ChatKit requires a client_secret JWT token that includes:
    - user_id: The authenticated user's ID
    - exp: Token expiration time
    - workflow_id: The ChatKit workflow ID (from config)

    This endpoint generates and signs the JWT using the OpenAI API key.
    """

    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-openai-api-key-here":
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in .env"
        )

    if not settings.CHATKIT_WORKFLOW_ID or settings.CHATKIT_WORKFLOW_ID == "your-chatkit-workflow-id-here":
        raise HTTPException(
            status_code=503,
            detail="ChatKit workflow ID not configured. Please set CHATKIT_WORKFLOW_ID in .env"
        )

    # Create JWT payload for ChatKit
    # ChatKit expects specific claims for authentication
    payload = {
        "sub": str(current_user.user_id),  # Subject: user identifier
        "exp": int(time.time()) + 3600,     # Expires in 1 hour
        "iat": int(time.time()),            # Issued at
        "workflow_id": settings.CHATKIT_WORKFLOW_ID,  # ChatKit workflow
    }

    # Sign the JWT with OpenAI API key
    # ChatKit validates this token against the workflow configuration
    client_secret = jwt.encode(
        payload,
        settings.OPENAI_API_KEY,
        algorithm="HS256"
    )

    return {
        "client_secret": client_secret,
        "expires_in": 3600
    }
