"""
Database repository for chat operations.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.chat import Conversation, ChatMessage

async def get_conversation_history(
    db: AsyncSession,
    conversation_id: UUID,
    user_id: UUID,
    limit: int = 30
) -> List[ChatMessage]:
    """
    Retrieve the last N messages for a conversation.
    Verified for user ownership.
    """
    # Verify ownership and existence
    conv_check = await db.execute(
        select(Conversation).where(
            Conversation.conversation_id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    if not conv_check.scalar_one_or_none():
        return []

    # Get messages
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    messages = result.scalars().all()

    # Return in chronological order
    return sorted(messages, key=lambda x: x.created_at)

async def create_chat_message(
    db: AsyncSession,
    conversation_id: UUID,
    role: str,
    content: str,
    tool_call_id: Optional[str] = None
) -> ChatMessage:
    """
    Create and persist a new chat message.
    """
    message = ChatMessage(
        conversation_id=conversation_id,
        role=role,
        content=content,
        tool_call_id=tool_call_id
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message
