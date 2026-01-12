# Tasks: Phase III - Todo AI Chatbot

**Input**: Design documents from `/specs/003-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure for AI modules in `backend/src/agents/` and `backend/src/mcp/`
- [ ] T002 Update `backend/pyproject.toml` or `requirements.txt` with `openai-agents-python`, `mcp-sdk-python`, and `pyjwt`
- [ ] T003 [P] Configure environment variables for `OPENAI_API_KEY` and `BETTER_AUTH_SECRET` in `.env`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create database migrations for `Conversation` and `Message` tables in `backend/src/db/migrations/`
- [ ] T005 [P] Implement `Conversation` and `Message` SQLModel entities in `backend/src/db/models.py`
- [ ] T006 [P] Implement JWT validation dependency in `backend/src/auth/jwt.py` sharing `BETTER_AUTH_SECRET`
- [ ] T007 Setup the core MCP server entry point in `backend/src/mcp/server.py`
- [ ] T008 [P] Initialize the OpenAI Agent runner in `backend/src/agents/runner.py`
- [ ] T009 Create the ChatKit session initialization route in `backend/src/api/chatkit.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Conversational Task Management (Priority: P1) 🎯 MVP

**Goal**: Allow users to add, list, and complete tasks using natural language.

**Independent Test**: Use the Chat interface to send "Add task test", verify DB persistence, and then ask "List my tasks" to see it returned.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Implement `add_task` tool in `backend/src/mcp/tools.py`
- [ ] T011 [P] [US1] Implement `list_tasks` tool in `backend/src/mcp/tools.py`
- [ ] T012 [P] [US1] Implement `complete_task` tool in `backend/src/mcp/tools.py`
- [ ] T013 [US1] Configure the Todo Agent system prompt for reactivity in `backend/src/agents/todo_agent.py`
- [ ] T014 [US1] Implement the message persistence logic in `backend/src/api/chat.py`
- [ ] T015 [US1] Integrate `@openai/chatkit-react` in `frontend/src/components/ChatWidget.tsx`
- [ ] T016 [US1] Connect `ChatWidget` to the backend `/api/chatkit/session` endpoint

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Persistent Conversation Context (Priority: P2)

**Goal**: AI remembers previous messages in the session to resolve entity references.

**Independent Test**: "Add task Alpha" -> "Change its description to Beta". Verify Alpha's description is updated.

### Implementation for User Story 2

- [ ] T017 [US2] Implement history retrieval service in `backend/src/db/repository.py` to fetch last 30 messages
- [ ] T018 [US2] Update `backend/src/api/chat.py` to inject retrieved history into the OpenAI Agent run
- [ ] T019 [US2] Ensure `Conversation` IDs are tracked and persisted in the frontend `localStorage` or session state

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Natural Language Task Cleanup (Priority: P3)

**Goal**: Remove tasks using inferred natural language (e.g., "Remove the dentist task").

**Independent Test**: Ask "Remove the task about the dentist" and verify the task with "dentist" in title/desc is deleted.

### Implementation for User Story 3

- [ ] T020 [P] [US3] Implement `delete_task` tool in `backend/src/mcp/tools.py`
- [ ] T021 [US3] Update Agent system prompt to handle ambiguous deletion intents with tool chain
- [ ] T022 [US3] Add "Deletion Successful" feedback message in `backend/src/agents/prompts.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Clarification and Feedback (Priority: P2)

**Goal**: Bot asks for more info when a request is ambiguous.

**Independent Test**: Ask "update the task" when multiple exist; bot must list options and wait for choice.

### Implementation for User Story 4

- [ ] T023 [US4] Implement `update_task` tool in `backend/src/mcp/tools.py`
- [ ] T024 [US4] Configure Agent reasoning to pause tool execution for user clarification in `backend/src/agents/todo_agent.py`

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T025 [P] Update `README.md` with Phase III setup instructions
- [ ] T026 Add error boundary for ChatKit stream failures in `frontend/src/components/ChatWidget.tsx`
- [ ] T027 [P] Security audit of `jwt.py` logic against `BETTER_AUTH_SECRET` leakage
- [ ] T028 Run `quickstart.md` validation to ensure end-to-end flow works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - Sequential in priority order (US1 -> US2 -> US3 -> US4)

### Parallel Opportunities

- T002, T003 can run in parallel.
- T005, T006, T008 in Foundational phase.
- Tools in User Story 1 (T010, T011, T012).

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Task Manage)
4. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add US 1 -> Chat Basic (Smallest viable increment)
3. Add US 2 -> Chat Memory
4. Add US 3/4 -> Cleanup & Polish
