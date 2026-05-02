---
description: Prime agent with codebase + local PRD/story context
argument-hint: [PRD-ID | STORY-ID | path-to-prd-or-story]
---

# Prime: Load Project Context

**Input**: $ARGUMENTS

## Objective

Build comprehensive understanding of this codebase + the active PRD/story context.

**Core Principle**: READ ONLY — no code written. Strictly analysis and context loading.

---

## Step 0: Load Local PRD/Story Context (if provided)

Resolve input:

| Input | Resolution |
|-------|-----------|
| `PRD-NNN` | Load `.agents/PRDs/PRD-NNN-*/PRD.md` + `index.md` + every story under `.agents/stories/PRD-NNN-*/` |
| `STORY-NNN` (with active PRD context) | Load that story file + parent PRD + sibling stories' frontmatter |
| Path to `PRD.md` | Load that PRD + index + its stories |
| Path to story `.md` | Load that story + parent PRD + sibling stories' frontmatter |
| Blank | List `.agents/PRDs/` and ask user which to load |

Extract from frontmatter:
- PRD: `id`, `slug`, `status`, `base_branch`, `epic_branch`
- Story: `id`, `status`, `branch`, `plan`, `depends_on`, `blocks`, `complexity`

Read story bodies for: description, acceptance criteria, technical notes.

---

## Step 1: Analyze the Codebase

1. Read `backend/AGENTS.md` for backend conventions/architecture (if exists)
2. Read `frontend/AGENTS.md` if exists, else inspect `frontend/src/`
3. Backend structure: routers, services, repositories, models, schemas
4. Frontend structure: pages, components, layouts, lib
5. Check `frontend/package.json` for deps
6. Recent commits: `git log --oneline -5`
7. Current branch: `git branch --show-current`

---

## Output

Scannable summary:

- **Active PRD**: `{PRD-ID}` — {title} (status: {status})
- **Epic Branch**: `{epic_branch}` (base: `{base_branch}`)
- **Story Progress**: {done}/{total} done, {in-progress} in flight, {blocked} blocked
- **Active Story** (if specified): `{STORY-ID}` — {title} (status: {status}, branch: `{branch}`)
  - Acceptance criteria summary
  - Dependencies status (blocked-by satisfied? Y/N)
- **Project Purpose**: one sentence
- **Tech Stack**:
  - Frontend: React 19 + Vite + React Router 7, shadcn/ui, Tailwind v4, JavaScript
  - Backend: FastAPI + SQLAlchemy 2.x + Pydantic v2, SQLite, Uvicorn
- **Data Model**: core entities + relationships
- **Key Patterns**: backend layered (router → service → repository → model), frontend component/page structure
- **Current Git State**: branch + last 5 commits

Bullet points. Concise.
