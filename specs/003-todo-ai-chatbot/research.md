# Research: Phase III - Todo AI Chatbot

## 1. OpenAI Agents SDK + MCP Integration
**Decision**: Use `MCPServerStdio` for local development and `HostedMCPTool` patterns for the final agent.
**Rationale**: The official `openai-agents-python` SDK (2025) provides first-class support for MCP via context managers.
- Local development will use a subprocess (`MCPServerStdio`) to run the MCP server.
- The Agent will be initialized with a list of `mcp_servers`.
**Alternatives considered**:
- *Manual tool registration*: Rejected. MCP provides a standardized way to describe and invoke tools without manually writing JSON schemas in the agent definition.

## 2. OpenAI ChatKit Context & History
**Decision**: Use the `getClientSecret` pattern via a Next.js API route.
**Rationale**: By using `getClientSecret`, ChatKit communicates directly with OpenAI for the message stream after initial session creation, reducing backend overhead.
- History is persisted in Neon DB.
- Each new chat session request to `/api/chatkit` will fetch the last $N$ messages from the DB and pass them to the OpenAI "Runner" via the `messages` array.
**Alternatives considered**:
- *Proxy URL pattern*: Rejected as it requires the backend to handle every message chunk, increasing latency and complexity.

## 3. Better Auth + FastAPI JWT Validation
**Decision**: Use `PyJWT` with `HS256` signature verification sharing the `BETTER_AUTH_SECRET`.
**Rationale**: Better Auth tokens are standard HS256 signed JWTs. By sharing the secret key, FastAPI can validate the integrity of the token and extract the `sub` (user_id) without a database lookup or an external API call to the auth server.
**Alternatives considered**:
- *Remote introspection*: Rejected to maintain "stateless server" requirement.
- *Database-backed sessions*: Rejected to avoid extra DB round-trips for every API request where JWT verification suffices.

## Sources
- [How to Use MCP with OpenAI Agents - DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-mcp-with-openai-agents)
- [Model context protocol (MCP) - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/mcp/)
- [OpenAI Chatkit Integration Guide](https://www.buildwithmatija.com/blog/chatkit-nextjs-integration)
- [FastAPI Security - OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Better Auth JWT Strategy](https://www.better-auth.com/docs/concepts/session-management)
