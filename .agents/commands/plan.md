---
description: Create implementation plan for a single story
argument-hint: <path/to/story.md | STORY-ID>
---

# Implementation Plan Generator (per-story)

**Input**: $ARGUMENTS

## Objective

Transform a single story into a battle-tested implementation plan via codebase exploration. One plan per story (1:1).

**Core Principle**: PLAN ONLY — no code written to the application. Plan lives at `.agents/plans/{PRD-ID}/{STORY-ID}-{slug}.plan.md`.

**Order**: CODEBASE FIRST. Solutions must fit existing patterns.

---

## Phase 1: PARSE INPUT

Resolve input to a story file:

| Input | Action |
|-------|--------|
| Path to story `.md` | Load directly |
| `STORY-NNN` | Search `.agents/stories/*/STORY-NNN-*.md`. If multiple, ask user. |
| Path to PRD `.prd.md` (legacy) | Reject — must target a single story |
| Blank | List in-progress/todo stories, ask user |

Read story frontmatter:
- `id`, `prd`, `slug`, `title`, `type`, `complexity`
- `branch`, `base_branch`
- `depends_on`, `blocks`
- `status` (must be `todo` or `in-progress`)

If `status: blocked` → STOP, report blocker.

If `depends_on` non-empty, verify each dependency `status: done`. If not, warn user and ask whether to proceed.

Read parent PRD for architecture context: `.agents/PRDs/{prd}/PRD.md`.

---

## Phase 2: EXPLORE

### Study the Codebase

Use Explore agent to find:

1. **Similar implementations** — analogous features with file:line refs
2. **Naming conventions** — actual examples
3. **Error handling patterns** — how errors are created/handled
4. **Type definitions** — relevant interfaces/types
5. **Test patterns** — test file structure + assertions

### Document Patterns

| Category | File:Lines | Pattern |
|----------|------------|---------|
| NAMING | `path/to/file.py:10-15` | {description} |
| ERRORS | `path/to/file.py:20-30` | {description} |
| SCHEMAS | `path/to/schemas.py:1-10` | {description} |
| COMPONENTS | `frontend/src/components/X.jsx:1-25` | {description} |

---

## Phase 3: DESIGN

- Files to CREATE
- Files to UPDATE
- Dependency order
- Risks + mitigations

---

## Phase 4: GENERATE

### Plan File Path

`.agents/plans/{PRD-ID}/{STORY-ID}-{slug}.plan.md`

```bash
mkdir -p .agents/plans/{PRD-ID}
```

### Plan Template

```markdown
---
story: {STORY-ID}
prd: {PRD-ID}
slug: {kebab-slug}
title: {Story title}
type: {NEW_CAPABILITY | ENHANCEMENT | REFACTOR | BUG_FIX}
complexity: {LOW | MEDIUM | HIGH}
branch: {feature/PRD-NNN/STORY-NNN-slug}
base_branch: {epic branch}
created: {YYYY-MM-DD}
---

# Plan: {Story Title}

## Summary

{One paragraph: what we're building + approach}

## User Story

As a {user type}
I want to {action}
So that {benefit}

## Story Reference

- Story file: `.agents/stories/{PRD-ID}/{STORY-ID}-{slug}.md`
- PRD: `.agents/PRDs/{PRD-ID}/PRD.md`

## Metadata

| Field | Value |
|-------|-------|
| Type | {type} |
| Complexity | {LOW/MEDIUM/HIGH} |
| Systems Affected | {list} |
| Story | {STORY-ID} |
| PRD | {PRD-ID} |
| Branch | `{feature branch}` |
| Base Branch | `{epic branch}` |

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

Execute in order. Each task is atomic + verifiable.

### Task 1: {Description}

- **File**: `backend/app/models/resource.py`
- **Action**: CREATE / UPDATE
- **Implement**: {what to do}
- **Mirror**: `backend/app/models/Entity.py:lines` — follow this pattern
- **Validate**: `cd backend && uvicorn app.main:app --reload` (server starts without error)

### Task 2: {Description}

- **File**: `frontend/src/pages/Resource.jsx`
- **Action**: CREATE / UPDATE
- **Implement**: {what to do}
- **Mirror**: `frontend/src/pages/ExistingPage.jsx:lines`
- **Validate**: `cd frontend && npm run lint`

{Continue for each task...}

---

## End-to-End Tests

List manual/automated E2E checks for `/implement` to execute:

- [ ] Start backend, hit `GET /resource` → returns 200 + expected shape
- [ ] Start frontend, navigate to /resource page → renders correctly
- [ ] {Other E2E checks}

---

## Validation

```bash
cd frontend && npm run lint
curl http://localhost:8000/health
```

---

## Acceptance Criteria

(Copied from story `{STORY-ID}`)

- [ ] {AC 1}
- [ ] {AC 2}
- [ ] All tasks completed
- [ ] Frontend lint passes
- [ ] Backend server starts without error
- [ ] Follows existing patterns
```

---

## Phase 5: UPDATE STORY FILE

After plan written, update the story file frontmatter:

- Set `plan: .agents/plans/{PRD-ID}/{STORY-ID}-{slug}.plan.md`
- If `status: todo` → set `status: in-progress`
- Update `updated: {YYYY-MM-DD}`

Then regenerate `.agents/PRDs/{PRD-ID}/index.md` to reflect the new status + plan link.

---

## Phase 6: OUTPUT

```markdown
## Plan Created

**Story**: {STORY-ID} — {title}
**File**: `.agents/plans/{PRD-ID}/{STORY-ID}-{slug}.plan.md`

**Summary**: {2-3 sentences}

**Scope**:
- {N} files to CREATE
- {M} files to UPDATE
- {K} total tasks

**Key Patterns**:
- {Pattern 1 with file:line}
- {Pattern 2 with file:line}

**Story Status**: todo → in-progress
**Index**: regenerated at `.agents/PRDs/{PRD-ID}/index.md`

**Next Step**: `/implement .agents/plans/{PRD-ID}/{STORY-ID}-{slug}.plan.md`
```
