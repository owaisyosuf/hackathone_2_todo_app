---
description: "Task list for In-Memory Todo Console Application"
---

# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Unit and integration tests will be included to ensure all functionality works as specified.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are generated based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks are organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with src/, tests/ directories
- [x] T002 [P] Create src/models/ directory for task entity
- [x] T003 [P] Create src/services/ directory for task operations
- [x] T004 [P] Create src/cli/ directory for console interface
- [x] T005 [P] Create tests/unit/ directory for unit tests
- [x] T006 [P] Create tests/integration/ directory for integration tests
- [x] T007 [P] Create contracts/ directory for API contracts

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create Task class/model in src/models/task.py with id, title, description, completed fields
- [x] T009 [P] Create in-memory storage mechanism in src/models/task.py (dictionary for tasks, counter for next ID)
- [x] T010 Create TaskService class in src/services/task_service.py with business logic methods
- [x] T011 [P] Implement add_task method in TaskService with validation
- [x] T012 [P] Implement get_all_tasks method in TaskService
- [x] T013 [P] Implement get_task_by_id method in TaskService
- [x] T014 [P] Implement update_task method in TaskService
- [x] T015 [P] Implement delete_task method in TaskService
- [x] T016 [P] Implement toggle_task_completion method in TaskService
- [ ] T017 Create error handling utilities in src/utils/errors.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to create a new todo task with a unique ID and mark it as incomplete by default

**Independent Test**: Can be fully tested by running the application, selecting "Add Task", entering a title, and verifying that a new task with a unique ID appears in the task list and is marked as incomplete.

### Tests for User Story 1 (TDD approach)
- [ ] T018 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [ ] T019 [P] [US1] Unit test for add_task method in tests/unit/test_task_service.py
- [ ] T020 [P] [US1] Contract test for add task functionality in tests/contract/test_add_task.py

### Implementation for User Story 1
- [x] T021 [P] [US1] Implement Task model with validation in src/models/task.py
- [x] T022 [US1] Create main application loop in src/cli/main.py
- [x] T023 [US1] Implement add task functionality in src/cli/main.py
- [x] T024 [US1] Add input validation for task title in src/cli/main.py
- [x] T025 [US1] Add error handling for empty titles in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: Enable users to see all their existing tasks with unique IDs, titles, descriptions, and completion status

**Independent Test**: Can be fully tested by adding some tasks and then selecting "View Tasks" to confirm all tasks are displayed with their details.

### Tests for User Story 2 (TDD approach)
- [ ] T026 [P] [US2] Unit test for get_all_tasks method in tests/unit/test_task_service.py
- [ ] T027 [P] [US2] Unit test for get_task_by_id method in tests/unit/test_task_service.py
- [ ] T028 [P] [US2] Contract test for view tasks functionality in tests/contract/test_view_tasks.py

### Implementation for User Story 2
- [x] T029 [P] [US2] Implement get_all_tasks method in src/services/task_service.py
- [x] T030 [US2] Implement view tasks functionality in src/cli/main.py
- [x] T031 [US2] Format task display with ID, title, description, and status in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P3)

**Goal**: Allow users to modify an existing task's title or description by selecting a task by ID

**Independent Test**: Can be fully tested by creating a task, selecting "Update Task", choosing the task by ID, and modifying its title or description.

### Tests for User Story 3 (TDD approach)
- [ ] T032 [P] [US3] Unit test for update_task method in tests/unit/test_task_service.py
- [ ] T033 [P] [US3] Contract test for update task functionality in tests/contract/test_update_task.py

### Implementation for User Story 3
- [x] T034 [P] [US3] Implement update_task method in src/services/task_service.py
- [x] T035 [US3] Implement update task functionality in src/cli/main.py
- [x] T036 [US3] Add validation for task existence in src/cli/main.py
- [x] T037 [US3] Add validation for updated title in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: Allow users to remove completed or unwanted tasks by selecting a task by ID

**Independent Test**: Can be fully tested by creating a task, selecting "Delete Task", choosing the task by ID, and confirming it no longer appears in the task list.

### Tests for User Story 4 (TDD approach)
- [ ] T038 [P] [US4] Unit test for delete_task method in tests/unit/test_task_service.py
- [ ] T039 [P] [US4] Contract test for delete task functionality in tests/contract/test_delete_task.py

### Implementation for User Story 4
- [x] T040 [P] [US4] Implement delete_task method in src/services/task_service.py
- [x] T041 [US4] Implement delete task functionality in src/cli/main.py
- [x] T042 [US4] Add validation for task existence in src/cli/main.py

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

**Goal**: Enable users to track completed tasks by selecting a task by ID and toggling its completion status

**Independent Test**: Can be fully tested by creating a task, selecting "Toggle Complete", choosing the task by ID, and verifying its completion status changes.

### Tests for User Story 5 (TDD approach)
- [ ] T043 [P] [US5] Unit test for toggle_task_completion method in tests/unit/test_task_service.py
- [ ] T044 [P] [US5] Contract test for toggle completion functionality in tests/contract/test_toggle_completion.py

### Implementation for User Story 5
- [x] T045 [P] [US5] Implement toggle_task_completion method in src/services/task_service.py
- [x] T046 [US5] Implement toggle completion functionality in src/cli/main.py
- [x] T047 [US5] Add validation for task existence in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Console Interface & Menu System

**Goal**: Provide clear menu options and handle user inputs gracefully

- [x] T048 Create main menu system in src/cli/main.py with all five options
- [x] T049 [P] Implement menu navigation logic in src/cli/main.py
- [x] T050 [P] Implement user input handling with error validation in src/cli/main.py
- [x] T051 [P] Add graceful error handling for invalid inputs in src/cli/main.py
- [x] T052 [P] Implement application exit functionality in src/cli/main.py

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T053 [P] Add comprehensive error handling across all modules
- [x] T054 [P] Add input validation for all user inputs
- [x] T055 [P] Add docstrings to all functions and classes
- [ ] T056 [P] Add logging for application events
- [ ] T057 [P] Create integration tests in tests/integration/test_cli_flow.py
- [x] T058 [P] Run quickstart validation to ensure all features work together
- [x] T059 [P] Code cleanup and refactoring

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Console Interface (Phase 8)**: Depends on all user story implementations
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services (T021 before T022, etc.)
- Services before CLI interface
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 8: Basic console interface for US1
5. **STOP and VALIDATE**: Test User Story 1 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 + tests
   - Developer B: User Story 2 + tests
   - Developer C: User Story 3 + tests
   - Developer D: User Story 4 + tests
   - Developer E: User Story 5 + tests
3. Console interface and integration work after all stories are complete
4. Stories complete and integrate independently

---