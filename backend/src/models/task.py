"""
Task database model.

Represents a todo item owned by a specific user.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.database import Base


class Task(Base):
    """
    Task model for todo items.

    Attributes:
        task_id: Unique identifier (UUID)
        user_id: Foreign key to User (owner)
        title: Task title (required, max 200 chars)
        description: Optional detailed description
        is_completed: Completion status (default: False)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "tasks"

    task_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    is_completed = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship to User
    user = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(task_id={self.task_id}, title={self.title}, completed={self.is_completed})>"
