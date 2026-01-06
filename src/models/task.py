"""
Task model for the Todo Console Application.

This module defines the Task class and in-memory storage mechanism.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo task in the system.

    Attributes:
        id: Unique identifier for the task
        title: Title of the task (required, non-empty)
        description: Optional description of the task
        completed: Completion status of the task (default: False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 255:
            raise ValueError("Task title cannot exceed 255 characters")
        if len(self.description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")


class TaskStorage:
    """
    In-memory storage for tasks using a dictionary.
    """
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, task: Task) -> Task:
        """
        Add a task to storage with a unique ID.

        Args:
            task: The task to add

        Returns:
            The task with its assigned ID
        """
        task.id = self._next_id
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        return list(self._tasks.values())

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
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            if len(title) > 255:
                raise ValueError("Task title cannot exceed 255 characters")
            task.title = title

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Task description cannot exceed 1000 characters")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated task if found, None otherwise
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        task.completed = not task.completed
        return task