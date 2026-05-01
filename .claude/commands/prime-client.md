---
description: Prime agent with client/frontend codebase understanding
argument-hint: [jira-issues] [confluence-pages]
---

# Prime Client: Load Frontend Context

**Input**: $ARGUMENTS

## Objective

Build comprehensive understanding of the client codebase by analyzing structure and key files.

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

1. Study the pages (`frontend/src/pages/`) — route-level components
2. Study the layouts (`frontend/src/layouts/`) — shared layout wrappers
3. Study the shared UI primitives (`frontend/src/components/`) — reusable components
4. Check `frontend/package.json` for dependencies

## Output

Produce a scannable summary of what you learned:

- **Purpose**: What the UI does
- **Tech Stack**: React 19 + Vite + React Router 7, shadcn/ui, Tailwind v4, JavaScript (no TypeScript)
- **Components**: Key components and their responsibilities
- **Data Flow**: Client-side React components fetch from FastAPI backend (`http://localhost:8000/api/v1`); all components are client-side (no Server Components)
- **Patterns**: How routing is structured with React Router 7, how components call the API, how forms handle state

Use bullet points. Keep it concise.
