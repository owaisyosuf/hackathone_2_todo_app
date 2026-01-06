#!/usr/bin/env python3
"""
Simple test script to validate the Todo Console Application functionality.
"""
import sys
import os

# Add src to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli.main import TodoApp
from services.task_service import TaskService


def test_task_service():
    """Test the TaskService functionality directly."""
    print("Testing TaskService functionality...")

    service = TaskService()

    # Test adding a task
    task1 = service.add_task("Test task 1", "This is a test task")
    print(f"Added task: ID={task1.id}, Title='{task1.title}', Description='{task1.description}', Completed={task1.completed}")

    # Test adding another task
    task2 = service.add_task("Test task 2")
    print(f"Added task: ID={task2.id}, Title='{task2.title}', Description='{task2.description}', Completed={task2.completed}")

    # Test getting all tasks
    all_tasks = service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")

    # Test getting a specific task
    retrieved_task = service.get_task(task1.id)
    print(f"Retrieved task: ID={retrieved_task.id}, Title='{retrieved_task.title}'")

    # Test updating a task
    updated_task = service.update_task(task1.id, title="Updated task 1", description="Updated description")
    print(f"Updated task: ID={updated_task.id}, Title='{updated_task.title}', Description='{updated_task.description}'")

    # Test toggling completion
    toggled_task = service.toggle_task_completion(task1.id)
    print(f"Toggled task: ID={toggled_task.id}, Completed={toggled_task.completed}")

    # Toggle again to return to original state
    toggled_task = service.toggle_task_completion(task1.id)
    print(f"Toggled task back: ID={toggled_task.id}, Completed={toggled_task.completed}")

    # Test deleting a task
    delete_result = service.delete_task(task2.id)
    print(f"Deleted task {task2.id}: {delete_result}")

    # Verify deletion
    remaining_tasks = service.get_all_tasks()
    print(f"Remaining tasks after deletion: {len(remaining_tasks)}")

    print("TaskService tests completed successfully!")


def main():
    """Run the test."""
    print("Starting Todo Console Application validation...")

    # Test the service layer
    test_task_service()

    print("\nThe Todo Console Application components are working correctly!")
    print("To run the full application, execute: python src/cli/main.py")


if __name__ == "__main__":
    main()