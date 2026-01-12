# Feature Specification: Phase III - Todo AI Chatbot

**Feature Branch**: `003-todo-ai-chatbot`
**Created**: 2026-01-12
**Status**: Draft
**Input**: User description: "Phase III: Todo AI Chatbot"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conversational Task Management (Priority: P1)

A user wants to manage their todo list using natural language conversations instead of clicks and forms. They should be able to say things like "Add a task to buy groceries" or "Show me what I have to do today" and have the system respond appropriately.

**Why this priority**: This is the core value proposition of Phase III - the transition to an agentic conversational interface.

**Independent Test**: Can be tested by sending natural language prompts (Add/List) via the ChatKit UI and observing that the system correctly interprets the intent and performs the requested action.

**Acceptance Scenarios**:

1. **Given** a user is logged into the chat interface, **When** they type "Remind me to call John at 5pm", **Then** the system confirms the task has been added and lists it as a pending task.
2. **Given** a user has multiple tasks, **When** they ask "What are my pending tasks?", **Then** the system returns a list of all incomplete tasks.
3. **Given** an existing task "buy milk", **When** the user says "I've bought the milk", **Then** the system marks the task as completed.

---

### User Story 2 - Persistent Conversation Context (Priority: P2)

A user wants the chatbot to remember what they were talking about previously. If they ask "Tell me more about the grocery task", the system should know which "grocery task" they mean based on the previous message in the conversation.

**Why this priority**: Conversation history is essential for a "natural" feeling AI. Without context, users have to repeat themselves constantly.

**Independent Test**: Send a sequence of messages where the second message refers to an entity in the first (e.g., "Add task X" then "Complete it") and verify "it" is resolved correctly.

**Acceptance Scenarios**:

1. **Given** a previous message about a task named "Project Alpha", **When** the user asks "Set the description for that task to 'high priority'", **Then** the system updates "Project Alpha".
2. **Given** a user returns to a conversation after refreshing the page, **When** they ask "What did we last talk about?", **Then** the system provides a summary based on the stored history.

---

### User Story 3 - Natural Language Task Cleanup (Priority: P3)

A user wants to clean up their list using conversational commands like "Delete all my completed tasks" or "Remove the task about the dentist".

**Why this priority**: Enhances the power of the natural language interface by allowing bulk or inferred operations that are faster than manual UI clicks.

**Independent Test**: Add multiple completed tasks, ask the bot to delete all completed tasks, and verify the task list is cleaned up.

**Acceptance Scenarios**:

1. **Given** multiple tasks marked as completed, **When** the user says "Clean up my completed tasks", **Then** the system invokes the delete tool for all completed tasks.
2. **Given** a task "Cancel dentist appointment", **When** the user says "Remove the dentist task", **Then** the system identifies and deletes the correct task.

---

### User Story 4 - Clarification and Feedback (Priority: P2)

A user wants the bot to ask for more info if a request is ambiguous. If they say "update the task", but they have three tasks, the bot should ask *which* task they want to update.

**Why this priority**: Prevents destructive actions on wrong tasks and builds trust with the user.

**Independent Test**: Provoke an ambiguous command (e.g., "complete task" when multiple exist) and verify the bot asks a clarifying question instead of guessing.

**Acceptance Scenarios**:

1. **Given** two tasks containing the word "Report", **When** the user says "Complete the report task", **Then** the system lists both tasks and asks for clarification.

---

### Edge Cases

- **What happens when the LLM misinterprets a command?** The system should provide a clear summary of what it *did* do, allowing the user to say "No, I meant..." or undo the action (via manual tool invocation or correction).
- **How does the system handle concurrent messages in one conversation?** The backend must handle message sequences strictly and ensure the "stateless" agent always has the latest DB-persisted state before responding.
- **What happens if a tool call fails (e.g., DB down)?** The agent should inform the user that it encountered a technical issue while performing the action.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a natural language chat interface using OpenAI ChatKit.
- **FR-002**: System MUST use an OpenAI Agent with access to specific MCP tools for task management.
- **FR-003**: System MUST persist every message (User and Assistant) in the Neon PostgreSQL database.
- **FR-004**: System MUST retrieve and provide the conversation history to the Agent on every turn to maintain context.
- **FR-005**: System MUST implement stateless Tooling (MCP) that interacts directly with the database.
- **FR-011**: System MUST be strictly reactive, only performing actions or responding to explicit user instructions.
- **FR-012**: System MUST provide the full message history of the current conversation (retrieved from database) to the Agent on each request to maintain continuity.
- **FR-013**: System MUST authenticate all Chat API requests using stateless JWT tokens validated against Better Auth.

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item (Title, Description, Status, UserID).
- **Conversation**: Represents a session between a User and the AI.
- **Message**: An individual text entry in a Conversation (Role: User/Assistant/System/Tool, Content, Timestamp).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add, list, and complete tasks via natural language with 90%+ intent recognition accuracy for standard commands.
- **SC-002**: The Chat interface loads and displays the first message from the history in under 2 seconds.
- **SC-003**: 95% of tool-invoked task operations (Add/Update/Delete) are persisted to the database in under 500ms (excluding LLM latency).
- **SC-004**: Users are able to resolve ambiguity in under 2 turns when the bot asks for clarification.
- **SC-005**: All conversation state is recoverable; a page refresh restores the exact text and task context of the previous turn.

### Assumptions
- Better Auth will provide the `user_id` context for all Chat API calls.
- OpenAI ChatKit will handle the primary UI rendering and state.
- Neon PostgreSQL latency is within standard cloud expectations for serverless DBs.
