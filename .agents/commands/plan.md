---
description: Create implementation plan with codebase analysis
argument-hint: <feature description | path/to/prd.md>
---

# Implementation Plan Generator

**Input**: $ARGUMENTS

## Objective

Transform the input into a battle-tested implementation plan through codebase exploration and pattern extraction.

**Core Principle**: PLAN ONLY - no code written to the application. This command creates a plan document in `.agents/plans/` that will later be executed by the `/implement` command.

**Order**: CODEBASE FIRST. Solutions must fit existing patterns.

---

## Phase 1: PARSE

### Determine Input Type

| Input | Action |
|-------|--------|
| `.prd.md` file | Read PRD, extract next pending phase |
| Other `.md` file | Read and extract feature description |
| Free-form text | Use directly as feature input |
| Blank | Use conversation context |

### Extract Feature Understanding

- **Problem**: What are we solving?
- **User Story**: As a [user], I want to [action], so that [benefit]
- **Type**: NEW_CAPABILITY / ENHANCEMENT / REFACTOR / BUG_FIX
- **Complexity**: LOW / MEDIUM / HIGH
- **Jira Issue**: If a Jira issue key (e.g., `RH-5`) is available in the conversation context — from a prior `/prime` command, user mention, or PRD — capture it. This is optional but should be included in the plan metadata when available so that `/implement` can update the issue after completion.

---

## Phase 2: EXPLORE

### Study the Codebase

Use the Explore agent to find:

1. **Similar implementations** - analogous features with file:line references
2. **Naming conventions** - actual examples from the codebase
3. **Error handling patterns** - how errors are created and handled
4. **Type definitions** - relevant interfaces and types
5. **Test patterns** - test file structure and assertion styles

### Document Patterns

| Category | File:Lines | Pattern |
|----------|------------|---------|
| NAMING | `path/to/file.py:10-15` | {pattern description} |
| ERRORS | `path/to/file.py:20-30` | {pattern description} |
| SCHEMAS | `path/to/schemas.py:1-10` | {pattern description} |
| COMPONENTS | `frontend/src/components/X.jsx:1-25` | {pattern description} |

---

## Phase 3: DESIGN

### Map the Changes

- What files need to be created?
- What files need to be modified?
- What's the dependency order?

### Identify Risks

| Risk | Mitigation |
|------|------------|
| {potential issue} | {how to handle} |

---

## Phase 4: GENERATE

### Create Plan File

**Output path**: `.agents/plans/{kebab-case-name}.plan.md`

```bash
mkdir -p .agents/plans
```

```markdown
# Plan: {Feature Name}

## Summary

{One paragraph: What we're building and approach}

## User Story

As a {user type}
I want to {action}
So that {benefit}

## Metadata

| Field | Value |
|-------|-------|
| Type | {type} |
| Complexity | {LOW/MEDIUM/HIGH} |
| Systems Affected | {list} |
| Jira Issue | {issue key if available, e.g. RH-5, or "N/A"} |

---

## Patterns to Follow

### Naming
```
// SOURCE: {file:lines}
{actual code snippet}
```

### Error Handling
```
// SOURCE: {file:lines}
{actual code snippet}
```

### Tests
```
// SOURCE: {file:lines}
{actual code snippet}
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/routers/resource.py` | CREATE | {why} |
| `frontend/src/pages/Resource.jsx` | CREATE | {why} |
| `path/to/other.py` | UPDATE | {why} |

---

## Tasks

Execute in order. Each task is atomic and verifiable.

### Task 1: {Description}

- **File**: `backend/app/models/resource.py`
- **Action**: CREATE / UPDATE
- **Implement**: {what to do}
- **Mirror**: `backend/app/models/Entity.py:lines` - follow this pattern
- **Validate**: `cd backend && uvicorn app.main:app --reload` (server starts without error)

### Task 2: {Description}

- **File**: `frontend/src/pages/Resource.jsx`
- **Action**: CREATE / UPDATE
- **Implement**: {what to do}
- **Mirror**: `frontend/src/pages/ExistingPage.jsx:lines`
- **Validate**: `cd frontend && npm run lint`

{Continue for each task...}

---

## Validation

```bash
# Frontend lint
cd frontend && npm run lint

# Backend smoke test
curl http://localhost:8000/health
```

---

## Acceptance Criteria

- [ ] All tasks completed
- [ ] Frontend lint passes
- [ ] Backend server starts without error
- [ ] Endpoint returns correct response (manual curl test)
- [ ] Follows existing patterns
```

---

## Phase 5: OUTPUT

```markdown
## Plan Created

**File**: `.agents/plans/{name}.plan.md`

**Summary**: {2-3 sentence overview}

**Scope**:
- {N} files to CREATE
- {M} files to UPDATE
- {K} total tasks

**Key Patterns**:
- {Pattern 1 with file:line}
- {Pattern 2 with file:line}

**Next Step**: Review the plan, then implement tasks in order.
```
