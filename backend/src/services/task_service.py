"""
Task service layer.

Handles task CRUD operations with user ownership verification.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import List
from uuid import UUID

from src.models.task import Task
from src.models.user import User
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse


async def create_task(
    task_data: TaskCreate,
    current_user: User,
    db: AsyncSession,
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Created task

    Example:
        >>> task = await create_task(
        ...     TaskCreate(title="Buy milk"),
        ...     current_user,
        ...     db
        ... )
    """
    new_task = Task(
        user_id=current_user.user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return TaskResponse.model_validate(new_task)


async def get_user_tasks(
    current_user: User,
    db: AsyncSession,
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        List[TaskResponse]: User's tasks

    Example:
        >>> tasks = await get_user_tasks(current_user, db)
        >>> print(len(tasks))
        5
    """
    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()

    return [TaskResponse.model_validate(task) for task in tasks]


async def get_task_by_id(
    task_id: UUID,
    current_user: User,
    db: AsyncSession,
) -> TaskResponse:
    """
    Get a specific task by ID with ownership verification.

    Args:
        task_id: Task's unique identifier
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Task details

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user

    Example:
        >>> task = await get_task_by_id(task_id, current_user, db)
    """
    result = await db.execute(
        select(Task).where(Task.task_id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    return TaskResponse.model_validate(task)


async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User,
    db: AsyncSession,
) -> TaskResponse:
    """
    Update a task with ownership verification.

    Args:
        task_id: Task's unique identifier
        task_data: Updated task data
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user

    Example:
        >>> task = await update_task(
        ...     task_id,
        ...     TaskUpdate(title="Buy milk and eggs"),
        ...     current_user,
        ...     db
        ... )
    """
    result = await db.execute(
        select(Task).where(Task.task_id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task",
        )

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title.strip()
    if task_data.description is not None:
        task.description = task_data.description.strip() if task_data.description else None

    await db.commit()
    await db.refresh(task)

    return TaskResponse.model_validate(task)


async def delete_task(
    task_id: UUID,
    current_user: User,
    db: AsyncSession,
) -> None:
    """
    Delete a task with ownership verification.

    Args:
        task_id: Task's unique identifier
        current_user: Authenticated user
        db: Database session

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user

    Example:
        >>> await delete_task(task_id, current_user, db)
    """
    result = await db.execute(
        select(Task).where(Task.task_id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task",
        )

    await db.delete(task)
    await db.commit()


async def toggle_task_completion(
    task_id: UUID,
    current_user: User,
    db: AsyncSession,
) -> TaskResponse:
    """
    Toggle task completion status with ownership verification.

    Args:
        task_id: Task's unique identifier
        current_user: Authenticated user
        db: Database session

    Returns:
        TaskResponse: Updated task with toggled status

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user

    Example:
        >>> task = await toggle_task_completion(task_id, current_user, db)
        >>> print(task.is_completed)
        True
    """
    result = await db.execute(
        select(Task).where(Task.task_id == task_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Verify ownership
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task",
        )

    # Toggle completion status
    task.is_completed = not task.is_completed

    await db.commit()
    await db.refresh(task)

    return TaskResponse.model_validate(task)
