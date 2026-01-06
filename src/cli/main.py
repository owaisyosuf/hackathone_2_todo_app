"""
Main CLI application for the Todo Console Application.

This module provides the console interface and menu system.
"""
import sys
import os
# Add src to the Python path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.task_service import TaskService
from src.models.task import Task
from typing import Optional


class TodoApp:
    """
    Main application class for the Todo Console Application.
    """
    def __init__(self):
        self._task_service = TaskService()
        self._running = True

    def run(self):
        """
        Run the main application loop.
        """
        print("Welcome to the Todo Console Application!")
        while self._running:
            self._show_menu()
            choice = self._get_user_input("Choose an option: ")
            self._handle_menu_choice(choice)

    def _show_menu(self):
        """
        Display the main menu options.
        """
        print("\nTodo Console Application")
        print("========================")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Complete")
        print("6. Exit")
        print()

    def _get_user_input(self, prompt: str) -> str:
        """
        Get input from the user with error handling.

        Args:
            prompt: The prompt to display to the user

        Returns:
            The user's input
        """
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nApplication interrupted. Exiting...")
            self._running = False
            return ""

    def _handle_menu_choice(self, choice: str):
        """
        Handle the user's menu choice.

        Args:
            choice: The user's menu choice
        """
        if choice == "1":
            self._add_task()
        elif choice == "2":
            self._view_tasks()
        elif choice == "3":
            self._update_task()
        elif choice == "4":
            self._delete_task()
        elif choice == "5":
            self._toggle_task_completion()
        elif choice == "6":
            self._exit()
        else:
            print("Invalid option. Please choose a number between 1-6.")

    def _add_task(self):
        """
        Handle adding a new task.
        """
        print("\n--- Add New Task ---")
        title = self._get_user_input("Enter task title: ")

        if not title:
            print("Error: Task title cannot be empty.")
            return

        description = self._get_user_input("Enter task description (optional): ")

        try:
            task = self._task_service.add_task(title, description)
            print(f"Task added successfully with ID {task.id}!")
        except ValueError as e:
            print(f"Error: {e}")

    def _view_tasks(self):
        """
        Handle viewing all tasks.
        """
        print("\n--- View All Tasks ---")
        tasks = self._task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print("Tasks:")
        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            print(f"ID: {task.id} | Title: {task.title} | Description: {task.description or 'None'} | Status: {status}")

    def _update_task(self):
        """
        Handle updating an existing task.
        """
        print("\n--- Update Task ---")
        task_id_str = self._get_user_input("Enter task ID to update: ")

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        task = self._task_service.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return

        print(f"Current task: {task.title}")
        new_title = self._get_user_input(f"Enter new title (current: '{task.title}', press Enter to keep current): ")
        new_description = self._get_user_input(f"Enter new description (current: '{task.description}', press Enter to keep current): ")

        # Use current values if user didn't enter new ones
        updated_title = new_title if new_title else None
        updated_description = new_description if new_description else None

        try:
            updated_task = self._task_service.update_task(task_id, updated_title, updated_description)
            if updated_task:
                print(f"Task {task_id} updated successfully!")
            else:
                print(f"Error: Failed to update task {task_id}.")
        except ValueError as e:
            print(f"Error: {e}")

    def _delete_task(self):
        """
        Handle deleting a task.
        """
        print("\n--- Delete Task ---")
        task_id_str = self._get_user_input("Enter task ID to delete: ")

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        success = self._task_service.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully!")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def _toggle_task_completion(self):
        """
        Handle toggling a task's completion status.
        """
        print("\n--- Toggle Task Completion ---")
        task_id_str = self._get_user_input("Enter task ID to toggle: ")

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        task = self._task_service.toggle_task_completion(task_id)
        if task:
            status = "Complete" if task.completed else "Incomplete"
            print(f"Task {task_id} status updated to: {status}")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def _exit(self):
        """
        Handle exiting the application.
        """
        print("Goodbye!")
        self._running = False


def main():
    """
    Main entry point for the application.
    """
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()