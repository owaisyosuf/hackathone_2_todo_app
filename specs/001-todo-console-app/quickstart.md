# Quickstart Guide: In-Memory Todo Console Application

**Date**: 2026-01-06
**Feature**: 001-todo-console-app

## Overview

This guide provides instructions for setting up and running the in-memory Python console Todo application. The application provides a simple interface for managing todo tasks in memory.

## Prerequisites

- Python 3.13 or higher
- No additional dependencies required (uses standard Python libraries only)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Verify Python Version
```bash
python --version
```
Ensure you have Python 3.13 or higher installed.

### 3. Navigate to the Project Directory
```bash
cd <project-root-directory>
```

## Running the Application

### 1. Execute the Application
```bash
python src/cli/main.py
```

### 2. Using the Application
Once the application starts, you'll see the main menu with the following options:
```
Todo Console Application
========================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
Choose an option:
```

## Feature Usage

### Add Task
1. Select option 1
2. Enter a task title (required)
3. Optionally enter a task description
4. The task will be created with a unique ID and marked as incomplete

### View Tasks
1. Select option 2
2. All tasks will be displayed with their ID, title, description, and completion status

### Update Task
1. Select option 3
2. Enter the task ID you want to update
3. Enter the new title (or press Enter to keep current)
4. Enter the new description (or press Enter to keep current)

### Delete Task
1. Select option 4
2. Enter the task ID you want to delete
3. The task will be permanently removed

### Toggle Complete
1. Select option 5
2. Enter the task ID you want to toggle
3. The completion status will be switched (completed ↔ incomplete)

### Exit
1. Select option 6
2. The application will terminate

## Example Workflow

```
Todo Console Application
========================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
Choose an option: 1
Enter task title: Buy groceries
Enter task description (optional): Milk, bread, eggs
Task added successfully with ID 1!

Todo Console Application
========================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
Choose an option: 2
Tasks:
ID: 1 | Title: Buy groceries | Description: Milk, bread, eggs | Status: Incomplete

Todo Console Application
========================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
Choose an option: 5
Enter task ID to toggle: 1
Task 1 status updated to: Complete

Todo Console Application
========================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
Choose an option: 2
Tasks:
ID: 1 | Title: Buy groceries | Description: Milk, bread, eggs | Status: Complete

Todo Console Application
========================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit
Choose an option: 6
Goodbye!
```

## Error Handling

The application handles errors gracefully:
- Invalid menu choices will show an error message and return to the main menu
- Invalid task IDs will show an error message
- Empty task titles will be rejected with an error message

## Troubleshooting

### Python Version Issues
If you encounter issues with Python version, ensure you have Python 3.13 or higher installed.

### File Not Found Errors
Ensure you're running the application from the project root directory and the file path is correct.

## Next Steps

After running the application successfully:
1. Test all five core features
2. Verify that tasks are properly stored in memory
3. Test error handling with invalid inputs
4. Review the code structure in src/ directory