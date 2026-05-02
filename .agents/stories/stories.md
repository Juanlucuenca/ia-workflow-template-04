# User Stories - AI Data Analysis Platform (Sprint 1)

This document contains the granular user stories derived from the PRD for the AI Data Analysis Platform.

## Phase 1: Estructura de Datos y Backend (Core)

### [STORY-001] Database Schema and Persistence (SQLite)
**Type**: Technical
**Jira Type**: Task
**Priority**: High
**Complexity**: Medium
**Phase**: Phase 1
**Labels**: `backend`, `database`, `sqlite`

#### Description
As a developer, I want to implement the SQLite database schema using SQLAlchemy so that we can persist chat sessions and message history locally.

#### Acceptance Criteria
- [ ] Given a FastAPI application, when it starts, then it should create/initialize a local SQLite database file.
- [ ] Given the `Sessions` model, it must include fields for `id` (UUID/Int), `title`, `created_at`, and `updated_at`.
- [ ] Given the `Messages` model, it must include fields for `id`, `session_id` (Foreign Key), `role` (user/assistant/system/tool), `content`, and `timestamp`.
- [ ] Given the repository pattern, then I should be able to create and retrieve sessions and messages from the DB.

#### Technical Notes
- Use SQLAlchemy for ORM.
- Follow the existing Repository/Service pattern in `backend/app`.
- Ensure `session_id` has a proper relationship and cascade delete if a session is removed.

#### Dependencies
- Blocks: STORY-002, STORY-003

---

### [STORY-002] PostgreSQL Connection and Data Access
**Type**: Technical
**Jira Type**: Task
**Priority**: High
**Complexity**: Small
**Phase**: Phase 1
**Labels**: `backend`, `database`, `postgresql`

#### Description
As a developer, I want to configure the connection to the external PostgreSQL database so that the agent can later query data for analysis.

#### Acceptance Criteria
- [ ] Given the `.env` file, when PostgreSQL credentials are provided, then the application should successfully establish a connection.
- [ ] Given a test script or endpoint, when executed, then it should confirm connectivity to the target PostgreSQL DB.
- [ ] Given the architecture, the PostgreSQL connection should be read-only for the agent's tools.

#### Technical Notes
- Use a separate SQLAlchemy engine or session factory for the PostgreSQL connection.
- Ensure the connection string is properly masked in logs.

#### Dependencies
- Blocked by: STORY-001
- Blocks: STORY-005

---

### [STORY-003] Session Management API
**Type**: Feature
**Jira Type**: Story
**Priority**: Medium
**Complexity**: Medium
**Phase**: Phase 1
**Labels**: `backend`, `api`

#### Description
As a user, I want to create and list chat sessions so that I can organize my analysis topics.

#### Acceptance Criteria
- [ ] Given the `GET /sessions` endpoint, when called, then it returns a list of all existing sessions sorted by most recent.
- [ ] Given the `POST /sessions` endpoint, when called with a title, then it creates a new session in the SQLite DB and returns the session object.
- [ ] Given the `GET /sessions/{id}/messages` endpoint, when called with a valid ID, then it returns the full message history for that session.

#### Technical Notes
- Implement standard FastAPI routers.
- Use Pydantic schemas for request/response validation.

#### Dependencies
- Blocked by: STORY-001
- Blocks: STORY-006

---

## Phase 2: El Agente Inteligente

### [STORY-004] Pydantic-AI and OpenRouter Integration
**Type**: Technical
**Jira Type**: Task
**Priority**: High
**Complexity**: Medium
**Phase**: Phase 2
**Labels**: `backend`, `ai`, `pydantic-ai`

#### Description
As a developer, I want to integrate Pydantic-AI with OpenRouter so that the application can interact with LLMs like Claude or GPT-4.

#### Acceptance Criteria
- [ ] Given the `backend` environment, when an OpenRouter API key is set, then the agent can send a prompt and receive a response.
- [ ] Given the Pydantic-AI agent definition, it must use a `SystemPrompt` that defines its role as a SQL Data Analyst.
- [ ] Given a basic test query, when sent to the agent, then it returns a valid text response.

#### Technical Notes
- Refer to `Pydantic-AI` documentation for tool-calling setup.
- Configure OpenRouter as the base URL for the OpenAI-compatible provider in Pydantic-AI.

#### Dependencies
- Blocks: STORY-005

---

### [STORY-005] Agent Tools for SQL Introspection and Querying
**Type**: Feature
**Jira Type**: Story
**Priority**: High
**Complexity**: Large
**Phase**: Phase 2
**Labels**: `backend`, `ai`, `postgresql`

#### Description
As a user, I want the agent to be able to list tables, see schemas, and execute SELECT queries so that I can get answers from my data.

#### Acceptance Criteria
- [ ] Given the agent, it must have a `get_tables` tool that returns a list of tables from PostgreSQL.
- [ ] Given the agent, it must have a `get_table_schema` tool that returns columns and types for a specific table.
- [ ] Given the agent, it must have an `execute_query` tool that:
    - Only allows `SELECT` statements.
    - Forces a `LIMIT 50`.
    - Handles SQL errors and provides feedback to the agent for auto-correction.
- [ ] Given a user question like "What tables do I have?", the agent should call `get_tables` and respond with the names.

#### Technical Notes
- Use the PostgreSQL connection from STORY-002.
- Implement strict SQL parsing or regex checks to prevent non-SELECT queries if possible, or rely on the agent's prompt + read-only DB user.

#### Dependencies
- Blocked by: STORY-002, STORY-004
- Blocks: STORY-006

---

## Phase 3: Frontend y Chat UI

### [STORY-006] Interactive Chat Interface
**Type**: Feature
**Jira Type**: Story
**Priority**: High
**Complexity**: Large
**Phase**: Phase 3
**Labels**: `frontend`, `ui`, `react`

#### Description
As a user, I want a clean chat interface so that I can interact with the AI agent naturally.

#### Acceptance Criteria
- [ ] Given the Home page, it should feature a chat window with an input field and a message list.
- [ ] Given a message from the user, it should be displayed immediately and sent to the backend.
- [ ] Given a response from the agent, it should be rendered using Markdown (supporting tables and code blocks).
- [ ] Given the sidebar, it should list recent sessions (from STORY-003) and allow switching between them.

#### Technical Notes
- Use Tailwind CSS for styling.
- Use `react-markdown` for rendering agent responses.
- Implement a `useChat` hook to manage state and API calls.

#### Dependencies
- Blocked by: STORY-003, STORY-005
- Blocks: STORY-007

---

## Phase 4: Validación y Pulido

### [STORY-007] UX Polish and Loading States
**Type**: Enhancement
**Jira Type**: Story
**Priority**: Medium
**Complexity**: Small
**Phase**: Phase 4
**Labels**: `frontend`, `ux`

#### Description
As a user, I want to see loading indicators while the agent is "thinking" or querying the database so that I know the app is working.

#### Acceptance Criteria
- [ ] Given an active request, a loading spinner or "typing" indicator should be visible.
- [ ] Given a long database result, the UI should handle scrolling and display elegantly.
- [ ] Given an error (network or agent failure), a user-friendly error message should appear.

#### Technical Notes
- Use Lucide React for icons.
- Implement optimistic updates for user messages if possible.

#### Dependencies
- Blocked by: STORY-006

---

### [STORY-008] SQL Auto-correction and Safety Validation
**Type**: Technical
**Jira Type**: Task
**Priority**: Medium
**Complexity**: Medium
**Phase**: Phase 4
**Labels**: `backend`, `ai`, `testing`

#### Description
As a developer, I want to verify that the agent can successfully correct its own SQL errors and that safety limits are strictly enforced.

#### Acceptance Criteria
- [ ] Given a query that fails due to a typo, when the agent receives the error, then it should retry with a corrected version.
- [ ] Given a query without a `LIMIT`, when executed by the tool, then it must include `LIMIT 50` in the final execution.
- [ ] Given a request for `DROP TABLE`, when the agent attempts it, then the tool must refuse or the prompt must prevent it.

#### Technical Notes
- Write integration tests that simulate these scenarios.
- Monitor agent logs to ensure the retry loop doesn't exceed 3-5 attempts.

#### Dependencies
- Blocked by: STORY-005
