#!/usr/bin/env python3
"""
Demo script that demonstrates all the Todo Console Application functionality.
"""
import sys
import os

# Add src to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_service import TaskService


def demo_all_features():
    """Demonstrate all features of the Todo Console Application."""
    print("Demo: Todo Console Application Features")
    print("="*40)

    # Create a fresh service instance
    service = TaskService()

    print("\n1. ADD TASK")
    print("-" * 15)
    task1 = service.add_task("Buy groceries", "Milk, bread, eggs, fruits")
    print(f"Added: '{task1.title}' (ID: {task1.id})")

    task2 = service.add_task("Walk the dog")
    print(f"Added: '{task2.title}' (ID: {task2.id})")

    task3 = service.add_task("Finish project report", "Complete the quarterly report for review")
    print(f"Added: '{task3.title}' (ID: {task3.id})")

    print("\n2. VIEW ALL TASKS")
    print("-" * 15)
    all_tasks = service.get_all_tasks()
    print(f"Total tasks: {len(all_tasks)}")
    for task in all_tasks:
        status = "Completed" if task.completed else "Incomplete"
        print(f"  ID {task.id}: {task.title} - {status}")
        if task.description:
            print(f"      Description: {task.description}")

    print("\n3. UPDATE TASK")
    print("-" * 15)
    updated_task = service.update_task(task2.id, title="Walk the dog in the morning", description="After breakfast")
    if updated_task:
        print(f"Updated task {task2.id}: '{updated_task.title}'")
        print(f"  New description: {updated_task.description}")

    print("\n4. TOGGLE COMPLETION")
    print("-" * 15)
    toggled_task = service.toggle_task_completion(task1.id)
    if toggled_task:
        status = "Completed" if toggled_task.completed else "Incomplete"
        print(f"Toggled task {task1.id}: Now {status}")

    # Toggle it back to original state
    toggled_task = service.toggle_task_completion(task1.id)
    status = "Completed" if toggled_task.completed else "Incomplete"
    print(f"Toggled task {task1.id} back: Now {status}")

    print("\n5. DELETE TASK")
    print("-" * 15)
    delete_result = service.delete_task(task3.id)
    if delete_result:
        print(f"Deleted task {task3.id}")

    print("\nFINAL STATE - All Remaining Tasks")
    print("-" * 30)
    remaining_tasks = service.get_all_tasks()
    print(f"Total remaining tasks: {len(remaining_tasks)}")
    for task in remaining_tasks:
        status = "Completed" if task.completed else "Incomplete"
        print(f"  ID {task.id}: {task.title} - {status}")

    print("\nAll five core features demonstrated successfully!")
    print("   1. Add Task")
    print("   2. View Tasks")
    print("   3. Update Task")
    print("   4. Delete Task")
    print("   5. Toggle Completion")


def main():
    """Run the demo."""
    print("Starting Todo Console Application demo...")
    demo_all_features()
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()