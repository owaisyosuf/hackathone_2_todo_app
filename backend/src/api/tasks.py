"""
Task management API endpoints.

Provides CRUD operations for user tasks with authentication.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.database import get_db
from src.auth.middleware import get_current_user
from src.models.user import User
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services import task_service

router = APIRouter(tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    **Authentication Required**: Bearer token

    **Request Body**:
    - title: Task title (1-200 characters, required)
    - description: Optional task description

    **Returns**:
    - 201: Created task with all details
    - 401: Unauthorized (invalid/missing token)
    - 422: Validation error
    """
    return await task_service.create_task(task_data, current_user, db)


@router.get(
    "",
    response_model=List[TaskResponse],
    summary="List all user tasks",
)
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user.

    **Authentication Required**: Bearer token

    **Returns**:
    - 200: List of user's tasks (ordered by created_at desc)
    - 401: Unauthorized (invalid/missing token)
    """
    return await task_service.get_user_tasks(current_user, db)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task details",
)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """
    Get details of a specific task.

    **Authentication Required**: Bearer token

    **Path Parameters**:
    - task_id: Task's unique identifier

    **Returns**:
    - 200: Task details
    - 401: Unauthorized (invalid/missing token)
    - 403: Forbidden (task not owned by user)
    - 404: Task not found
    """
    return await task_service.get_task_by_id(task_id, current_user, db)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """
    Update an existing task.

    **Authentication Required**: Bearer token

    **Path Parameters**:
    - task_id: Task's unique identifier

    **Request Body**:
    - title: New title (optional)
    - description: New description (optional, can be null to clear)

    **Returns**:
    - 200: Updated task
    - 401: Unauthorized (invalid/missing token)
    - 403: Forbidden (task not owned by user)
    - 404: Task not found
    - 422: Validation error
    """
    return await task_service.update_task(task_id, task_data, current_user, db)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a task.

    **Authentication Required**: Bearer token

    **Path Parameters**:
    - task_id: Task's unique identifier

    **Returns**:
    - 204: Task deleted successfully (no content)
    - 401: Unauthorized (invalid/missing token)
    - 403: Forbidden (task not owned by user)
    - 404: Task not found
    """
    await task_service.delete_task(task_id, current_user, db)


@router.patch(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    summary="Toggle task completion",
)
async def toggle_task_completion(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """
    Toggle the completion status of a task.

    **Authentication Required**: Bearer token

    **Path Parameters**:
    - task_id: Task's unique identifier

    **Returns**:
    - 200: Updated task with toggled status
    - 401: Unauthorized (invalid/missing token)
    - 403: Forbidden (task not owned by user)
    - 404: Task not found
    """
    return await task_service.toggle_task_completion(task_id, current_user, db)
