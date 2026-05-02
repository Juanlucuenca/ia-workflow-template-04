---
description: Learn how to build new API endpoints end-to-end
argument-hint: [jira-issues] [confluence-pages]
---

# Prime Endpoint: How to Build New Endpoints

**Input**: $ARGUMENTS

## Objective

Understand the full endpoint pattern from database to frontend so you can build new endpoints correctly.

## Process

### Step 0: Load External Context (if provided)

The first argument is an optional Jira issue key or comma-separated list of keys (e.g., `RH-5` or `RH-5,RH-6,RH-7`). The second argument is an optional Confluence page ID or comma-separated list of IDs (e.g., `123456` or `123456,789012`).

If Jira issues are provided:
1. Call `mcp__atlassian__getAccessibleAtlassianResources` to get the `cloudId`
2. For each issue key, call `mcp__atlassian__getJiraIssue` with `responseContentFormat: "markdown"` to fetch the issue summary, description, acceptance criteria, and any other relevant context
3. Use this context to inform your understanding of what work is expected

If Confluence page IDs are provided:
1. Call `mcp__atlassian__getAccessibleAtlassianResources` to get the `cloudId` (skip if already retrieved above)
2. For each page ID, call `mcp__atlassian__getConfluencePage` with `contentFormat: "markdown"` to fetch the page content
3. Use this context as additional background for understanding the project

### Step 1: Analyze the Codebase

Study the existing Entity resource as a complete reference (full data flow):

1. **Model**: `backend/app/models/Entity.py` — SQLAlchemy model extending `Base`
2. **Schema**: `backend/app/schemas/Entity.py` — Pydantic `EntityCreate`, `EntityUpdate`, `EntityRead`
3. **Repository**: `backend/app/repositories/Entity.py` — pure DB queries via SQLAlchemy, no HTTP concerns
4. **Service**: `backend/app/services/Entity.py` — business logic, uniqueness checks, raises `HTTPException`
5. **Router**: `backend/app/routers/Entity.py` — thin FastAPI router, calls service via `Depends(get_db)`
6. **Registration**: `backend/app/main.py` — how routers are registered with `app.include_router(..., prefix="/api/v1")`
7. **Frontend fetch**: a page in `frontend/src/pages/` — how the UI calls the backend REST API

## Output

Produce a scannable summary of what you learned:

- **Data Flow**: Router → Service → Repository → SQLAlchemy Model → SQLite
- **Validation**: Pydantic schemas in `schemas/` — `ResourceCreate`/`ResourceUpdate`/`ResourceRead` with `ConfigDict(from_attributes=True)`
- **Service Pattern**: Service calls repository, checks uniqueness, raises `HTTPException` (404/409)
- **Repository Pattern**: Pure DB functions using `SessionLocal`, never raises HTTP errors
- **Router Pattern**: Thin route handler, logs request, calls service, returns Pydantic schema
- **Frontend Pattern**: React component fetches `http://localhost:8000/api/v1/{resource}`, manages state with `useState`/`useEffect`

Use bullet points. Keep it concise.
