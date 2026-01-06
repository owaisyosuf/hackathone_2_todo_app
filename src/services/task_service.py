"""
Task Service for the Todo Console Application.

This module provides business logic for task operations.
"""
from typing import List, Optional
from src.models.task import Task, TaskStorage


class TaskService:
    """
    Provides business logic for task operations.
    """
    def __init__(self):
        self._storage = TaskStorage()

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task.

        Args:
            title: The title of the task (required)
            description: The description of the task (optional)

        Returns:
            The created task with a unique ID

        Raises:
            ValueError: If title is empty or exceeds length limits
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        if len(title) > 255:
            raise ValueError("Task title cannot exceed 255 characters")

        # Validate description
        if len(description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")

        # Create and store the task
        task = Task(id=0, title=title.strip(), description=description.strip())
        return self._storage.add_task(task)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self._storage.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks
        """
        return self._storage.get_all_tasks()

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Optional[Task]:
        """
        Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated task if found, None otherwise

        Raises:
            ValueError: If title is provided but is empty or exceeds length limits
        """
        return self._storage.update_task(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        return self._storage.delete_task(task_id)

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated task if found, None otherwise
        """
        return self._storage.toggle_task_completion(task_id)