# Phase III: Todo AI Chatbot Constitution

## 1. Objective
Build an AI-powered, natural-language Todo chatbot using Agentic Dev Stack and MCP (Model Context Protocol) architecture. The system must allow users to manage todos conversationally while maintaining a fully stateless backend with all state persisted in the database.

**Core Rule:**
Follow Agentic Dev Stack strictly: Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code.
❌ No manual coding.
✅ All implementation via Claude Code + Spec-Kit Plus.

## 2. Scope
- Conversational task creation, listing, updating, completion, and deletion.
- Natural language understanding for all task operations.
- Persistent conversation context via database.
- Stateless API design (no in-memory state).

## 3. Technology Stack (Mandatory)
| Component | Technology |
| :--- | :--- |
| Frontend | OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Logic | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth |

## 4. High-Level Architecture
1. User sends message via ChatKit UI.
2. FastAPI receives request at chat endpoint.
3. Conversation history fetched from DB.
4. OpenAI Agent is run with MCP tools.
5. Agent invokes MCP tools (stateless).
6. MCP tools persist data to DB.
7. Assistant response stored in DB.
8. Response returned to client.

**Key Rule:** Server must hold NO runtime state.

## 5. Database Models (Authoritative)
### Task
- `id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at`
### Conversation
- `id`, `user_id`, `created_at`, `updated_at`
### Message
- `id`, `user_id`, `conversation_id`, `role` (user | assistant), `content`, `created_at`

## 6. Chat API Specification
- **Endpoint:** `POST /api/{user_id}/chat`
- **Request:** `conversation_id` (optional), `message` (required).
- **Response:** `conversation_id`, `response`, `tool_calls`.

## 7. MCP Tooling Specification (Mandatory)
- `add_task`: Create task. Params: `user_id`, `title`, `description?`.
- `list_tasks`: Retrieve tasks. Params: `user_id`, `status` (all | pending | completed).
- `complete_task`: Mark task complete. Params: `user_id`, `task_id`.
- `delete_task`: Delete task. Params: `user_id`, `task_id`.
- `update_task`: Update task. Params: `user_id`, `task_id`, `title?`, `description?`.

**Rule:** MCP tools must be stateless and persist directly to DB.

## 8. Agent Behavior Rules (Non-Negotiable)
- Add / Remember → `add_task`
- Show / List → `list_tasks`
- Done / Complete → `complete_task`
- Delete / Remove → `delete_task`
- Change / Update → `update_task`
- Always confirm successful actions.
- Gracefully handle missing tasks.
- May chain multiple MCP tools in one turn.

## 9. Deliverables
- `/frontend` — ChatKit UI
- `/backend` — FastAPI + Agents SDK + MCP
- `/specs` — Agent + MCP specs
- Database migrations
- README with setup & deployment

## 10. Evaluation Criteria
- Spec completeness.
- Correct Agent → MCP interaction.
- Stateless correctness.
- Natural language coverage.
