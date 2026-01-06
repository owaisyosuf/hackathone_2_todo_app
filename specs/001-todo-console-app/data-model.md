# Data Model: In-Memory Todo Console Application

**Date**: 2026-01-06
**Feature**: 001-todo-console-app
**Input**: Feature specification requirements

## Overview

This document defines the data model for the in-memory Todo console application. It specifies the structure of the Task entity and the in-memory storage mechanism.

## Entity Definition

### Task

The Task entity represents a single todo item in the system.

**Fields**:
- `id`: Integer (required) - Unique identifier for the task, auto-generated as incrementing integer
- `title`: String (required) - Title of the task, must not be empty
- `description`: String (optional) - Optional description of the task, can be empty
- `completed`: Boolean (required) - Completion status of the task, defaults to False

**Validation Rules**:
- `id`: Must be a positive integer, unique across all tasks
- `title`: Must be a non-empty string with length between 1 and 255 characters
- `description`: Can be empty, maximum length of 1000 characters
- `completed`: Must be a boolean value (True or False)

**State Transitions**:
- Default state: `completed = False`
- State change: `completed` can be toggled between True and False

**Example**:
```python
task = {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "completed": False
}
```

## In-Memory Storage Model

### Task Repository

Tasks are stored in an in-memory dictionary where:
- Keys: Task IDs (integers)
- Values: Task objects (dictionaries with the structure defined above)

**Structure**:
```python
tasks = {
    1: {"id": 1, "title": "Buy groceries", "description": "Milk, bread, eggs", "completed": False},
    2: {"id": 2, "title": "Walk the dog", "description": "", "completed": True},
    3: {"id": 3, "title": "Finish report", "description": "Complete the quarterly report", "completed": False}
}
```

### ID Generation Strategy

- Start with ID = 1 for the first task
- For each new task, use the next available integer ID
- When a task is deleted, the ID is not reused (to maintain uniqueness)
- Track the next available ID in a separate variable

## Relationships

The Task entity is independent - there are no relationships between tasks in this simple todo application.

## Constraints

- Data exists only during application runtime (in-memory only)
- No persistence beyond application lifecycle
- Maximum recommended number of tasks: 10,000 (based on performance goals)
- All operations must maintain data integrity

## Operations

The data model supports these core operations:
- Create: Add a new task with auto-generated ID
- Read: Retrieve a task by ID
- Update: Modify task properties by ID
- Delete: Remove a task by ID
- List: Retrieve all tasks

## Validation Summary

- Task titles must not be empty
- Task IDs must be unique
- Only valid boolean values allowed for completion status
- Task must exist before update/delete operations