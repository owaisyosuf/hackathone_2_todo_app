"""
Task Pydantic schemas for API validation.

These schemas define the structure for task-related API requests and responses.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Attributes:
        title: Task title (required, 1-200 characters)
        description: Optional detailed description
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
            }
        }


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Attributes:
        title: Optional new title (1-200 characters)
        description: Optional new description (can be null to clear)
        is_completed: Optional completion status
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    is_completed: Optional[bool] = Field(None, description="Completion status")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and household items",
                "description": "Milk, eggs, bread, paper towels",
            }
        }


class TaskResponse(BaseModel):
    """
    Schema for task data in API responses.

    Attributes:
        task_id: Task's unique identifier
        user_id: Owner's user ID
        title: Task title
        description: Optional description
        is_completed: Completion status
        created_at: Creation timestamp
        updated_at: Last modification timestamp
    """

    task_id: UUID = Field(..., description="Task's unique identifier")
    user_id: UUID = Field(..., description="Owner's user ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    is_completed: bool = Field(..., description="Completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last modification timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "task_id": "660e8400-e29b-41d4-a716-446655440000",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "is_completed": False,
                "created_at": "2026-01-07T12:01:00Z",
                "updated_at": "2026-01-07T12:01:00Z",
            }
        }


class TaskToggle(BaseModel):
    """
    Schema for toggling task completion status.

    Attributes:
        is_completed: New completion status
    """

    is_completed: bool = Field(..., description="New completion status")

    class Config:
        json_schema_extra = {
            "example": {
                "is_completed": True,
            }
        }
