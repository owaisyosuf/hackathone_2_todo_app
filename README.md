# Todo Console Application

A Python-based console Todo application that stores all data in memory. The application provides five core features for managing todo tasks.

## Features

- **Add Task**: Create new todo tasks with titles and optional descriptions
- **View Tasks**: Display all existing tasks with their status
- **Update Task**: Modify existing task titles and descriptions
- **Delete Task**: Remove tasks from the list
- **Toggle Complete**: Mark tasks as complete/incomplete

## Requirements

- Python 3.13 or higher

## How to Run

To run the application:

```bash
python src/cli/main.py
```

## How to Use

The application provides a simple menu system:

1. **Add Task**: Enter a title (required) and description (optional)
2. **View Tasks**: See all tasks with their ID, title, description, and completion status
3. **Update Task**: Enter the task ID and provide new title/description
4. **Delete Task**: Enter the task ID to remove the task
5. **Toggle Complete**: Enter the task ID to switch completion status
6. **Exit**: Quit the application

## Architecture

The application follows a clean architecture with separation of concerns:

- **Models** (`src/models/`): Task entity and in-memory storage
- **Services** (`src/services/`): Business logic for task operations
- **CLI** (`src/cli/`): Console interface and menu system

## Implementation Details

- All data is stored in memory only (no persistence)
- Task IDs are auto-generated as incrementing integers
- Input validation prevents empty titles and handles errors gracefully
- The application handles invalid inputs without crashing

## Files

- `src/models/task.py`: Task model and in-memory storage
- `src/services/task_service.py`: Business logic for task operations
- `src/cli/main.py`: Console interface and main application loop
- `demo_tasks.py`: Demo script showing all functionality
- `test_app.py`: Test script to validate functionality