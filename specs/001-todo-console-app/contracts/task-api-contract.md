# Task Management API Contract

**Version**: 1.0
**Date**: 2026-01-06
**Feature**: 001-todo-console-app

## Overview

This contract defines the functional interfaces for the Todo console application. Although the application is console-based, this contract specifies the internal interfaces between components.

## Task Operations

### 1. Add Task

**Description**: Creates a new task with a unique ID

**Input**:
- title (string, required): Task title, must not be empty
- description (string, optional): Task description, can be empty

**Output**:
- task (object): Created task object with ID, title, description, and completion status
- success (boolean): Whether the operation was successful
- error (string, optional): Error message if operation failed

**Validation**:
- Title must not be empty
- Title must be less than 255 characters

### 2. View All Tasks

**Description**: Retrieves all tasks in the system

**Input**: None

**Output**:
- tasks (array): Array of all task objects
- count (integer): Number of tasks returned

### 3. View Task by ID

**Description**: Retrieves a specific task by its ID

**Input**:
- id (integer, required): Task ID to retrieve

**Output**:
- task (object): Task object if found
- success (boolean): Whether the operation was successful
- error (string, optional): Error message if operation failed

### 4. Update Task

**Description**: Updates an existing task's title and/or description

**Input**:
- id (integer, required): Task ID to update
- title (string, optional): New title (if provided)
- description (string, optional): New description (if provided)

**Output**:
- task (object): Updated task object
- success (boolean): Whether the operation was successful
- error (string, optional): Error message if operation failed

**Validation**:
- Task must exist
- If title is provided, it must not be empty

### 5. Delete Task

**Description**: Removes a task from the system

**Input**:
- id (integer, required): Task ID to delete

**Output**:
- success (boolean): Whether the operation was successful
- error (string, optional): Error message if operation failed

**Validation**:
- Task must exist

### 6. Toggle Task Completion

**Description**: Toggles the completion status of a task

**Input**:
- id (integer, required): Task ID to toggle

**Output**:
- task (object): Task object with updated completion status
- success (boolean): Whether the operation was successful
- error (string, optional): Error message if operation failed

**Validation**:
- Task must exist

## Data Models

### Task Object

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": false
}
```

**Fields**:
- id (integer): Unique identifier for the task
- title (string): Task title (required, non-empty)
- description (string): Task description (optional)
- completed (boolean): Completion status (default: false)

## Error Handling

All operations follow the same error handling pattern:

**Success Response**:
```json
{
  "success": true,
  "data": { ... }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

## Validation Rules

1. Task titles must not be empty
2. Task IDs must be positive integers
3. Task descriptions can be empty
4. Completion status must be boolean
5. Operations on non-existent tasks will return an error