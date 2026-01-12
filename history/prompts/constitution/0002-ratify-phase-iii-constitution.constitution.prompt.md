---
id: 0002
title: Ratify Phase III Todo AI Chatbot Constitution
stage: constitution
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 002-fullstack-web-app
user: default
command: /sp.constitution Phase III: Todo AI Chatbot — Constitution
labels: [constitution, phase-iii, ai-chatbot, mcp, agents-sdk]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution-phase-iii.md
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constituion Phase III: Todo AI Chatbot — Constitution
1. Objective

Build an AI-powered, natural-language Todo chatbot using Agentic Dev Stack and MCP (Model Context Protocol) architecture. The system must allow users to manage todos conversationally while maintaining a fully stateless backend with all state persisted in the database.

Core Rule:

Follow Agentic Dev Stack strictly: Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code

❌ No manual coding

✅ All implementation via Claude Code + Spec-Kit Plus

2. Scope (Basic Level Functionality)

The chatbot must support:

Conversational task creation, listing, updating, completion, and deletion

Natural language understanding for all task operations

Persistent conversation context via database

Stateless API design (no in-memory state)

3. Technology Stack (Mandatory)
Component    Technology
Frontend    OpenAI ChatKit
Backend    Python FastAPI
AI Logic    OpenAI Agents SDK
MCP Server    Official MCP SDK
ORM    SQLModel
Database    Neon Serverless PostgreSQL
Authentication    Better Auth
4. High-Level Architecture

Flow:

User sends message via ChatKit UI

FastAPI receives request at chat endpoint

Conversation history fetched from DB

OpenAI Agent is run with MCP tools

Agent invokes MCP tools (stateless)

MCP tools persist data to DB

Assistant response stored in DB

Response returned to client

Key Rule:

Server must hold NO runtime state

5. Database Models (Authoritative)
Task

id

user_id

title

description

completed

created_at

updated_at

Conversation

id

user_id

created_at

updated_at

Message

id

user_id

conversation_id

role (user | assistant)

content

created_at

6. Chat API Specification
Endpoint

POST /api/{user_id}/chat

Request
Field    Required    Description
conversation_id    No    Existing conversation ID (create new if missing)
message    Yes    User natural language input
Response
Field    Description
conversation_id    Conversation ID
response    Assistant reply
tool_calls    MCP tools invoked
7. MCP Tooling Specification (Mandatory)
add_task

Purpose: Create task

Params: user_id, title, description?

Returns: task_id, status, title

list_tasks

Purpose: Retrieve tasks

Params: user_id, status (all | pending | completed)

Returns: Array of tasks

complete_task

Purpose: Mark task complete

Params: user_id, task_id

Returns: task_id, status, title

delete_task

Purpose: Delete task

Params: user_id, task_id

Returns: task_id, status, title

update_task

Purpose: Update task

Params: user_id, task_id, title?, description?

Returns: task_id, status, title

Rule: MCP tools must be stateless and persist directly to DB.

8. Agent Behavior Rules (Non‑Negotiable)
Intent    Required Action
Add / Remember    add_task
Show / List    list_tasks
Done / Complete    complete_task
Delete / Remove    delete_task
Change / Update    update_task

Additional Rules:

Always confirm successful actions

Gracefully handle missing tasks

May chain multiple MCP tools in one turn

9. Stateless Conversation Cycle

Receive user message

Load conversation history from DB

Append new user message

Store message

Run agent with MCP tools

Execute tool calls

Store assistant message

Return response

10. Natural Language Coverage (Minimum)

The agent must correctly handle:

Add tasks

List all / pending / completed tasks

Complete tasks by ID or inference

Delete tasks by name or ID

Update task titles/descriptions

11. Frontend & Deployment (ChatKit)
Domain Allowlist (Required)

Deploy frontend (Vercel / GitHub Pages / Custom domain)

Add domain to OpenAI Security → Domain Allowlist

Obtain domain key

Environment Variable
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
12. Deliverables (Must Exist)

/frontend — ChatKit UI

/backend — FastAPI + Agents SDK + MCP

/specs — Agent + MCP specs

Database migrations

README with setup & deployment

13. Architectural Guarantees

Stateless backend

Horizontally scalable

Crash‑resilient

Conversation recovery after restart

MCP‑driven tool abstraction

14. Evaluation Criteria

Spec completeness

Correct Agent → MCP interaction

Stateless correctness

Natural language  this is my phase 3 summary check this summary and create and merge constitiution file

## Response snapshot

Ratifying Phase III: Todo AI Chatbot Constitution.
1. Created PHR: history/prompts/constitution/0002-ratify-phase-iii-constitution.constitution.prompt.md
2. Creating .specify/memory/constitution-phase-iii.md
3. Updating .specify/memory/constitution.md

## Outcome

- ✅ Impact: Established architectural principles for Phase III Agentic/MCP migration.
- 🧪 Tests: none (standard ratification)
- 📁 Files: .specify/memory/constitution-phase-iii.md, .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify Phase III: Todo AI Chatbot
- 🧠 Reflection: User provided a high-fidelity summary which forms the basis of the modular constitution for Phase III.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
