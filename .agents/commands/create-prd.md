---
description: Create a comprehensive Product Requirements Document (local file-based workflow)
argument-hint: [product-slug] [--base-branch main]
---

# Create PRD: Generate Product Requirements Document

## Overview

Generate a comprehensive PRD based on conversation context. Local file workflow — no Jira. Each PRD lives in its own directory with a status board (`index.md`) that tracks stories.

**Input**: $ARGUMENTS
- First arg: product slug (kebab-case). If absent, derive from PRD title.
- `--base-branch <name>`: base git branch for the epic (default: `main`).

---

## Phase 0: ASSIGN ID

1. List `.agents/PRDs/` directories matching `PRD-*`.
2. Find max numeric ID, increment by 1, zero-pad to 3 digits.
3. PRD ID format: `PRD-{NNN}-{kebab-slug}` (e.g. `PRD-001-user-auth`).
4. PRD directory: `.agents/PRDs/{PRD-ID}/`
5. Files to create:
   - `.agents/PRDs/{PRD-ID}/PRD.md` — main PRD doc with frontmatter
   - `.agents/PRDs/{PRD-ID}/index.md` — story status board (initially empty)

```bash
mkdir -p .agents/PRDs/{PRD-ID}
```

---

## PRD File Frontmatter

`PRD.md` MUST start with:

```yaml
---
id: PRD-{NNN}
slug: {kebab-slug}
title: {Product name}
status: draft           # draft | active | done | archived
base_branch: main       # base branch for the epic (override via --base-branch)
epic_branch: epic/PRD-{NNN}-{kebab-slug}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---
```

---

## PRD Structure

After frontmatter, generate these sections. Adapt depth to available info.

### Required Sections

**1. Executive Summary** — overview, value proposition, MVP goal (2-3 paragraphs)

**2. Mission** — mission statement + 3-5 core principles

**3. Target Users** — personas, technical level, needs/pain points

**4. MVP Scope** — In Scope / Out of Scope (checkboxes), grouped by category

**5. User Stories** — 5-8 stories in `As a [user], I want [action], so that [benefit]` format with examples

**6. Core Architecture & Patterns** — high-level architecture, directory structure, design patterns

**7. Tools/Features** — detailed feature specs

**8. Technology Stack** — backend/frontend tech with versions, dependencies

**9. Security & Configuration** — auth approach, env vars, in-scope/out-of-scope security

**10. API Specification** (if applicable) — endpoints, request/response, auth

**11. Success Criteria** — MVP definition, functional reqs (checkboxes), quality indicators

**12. Implementation Phases** — 3-4 phases with goal, deliverables, validation

**13. Future Considerations** — post-MVP enhancements

**14. Risks & Mitigations** — 3-5 risks with mitigation

**15. Appendix** (if applicable) — related docs, dependencies

---

## index.md Structure

Initial content:

```markdown
# {PRD-ID}: {Title} — Story Board

**PRD**: [PRD.md](./PRD.md)
**Epic Branch**: `epic/{PRD-ID}-{slug}` (base: `{base_branch}`)
**Status**: draft

## Stories

_No stories yet. Run `/create-stories .agents/PRDs/{PRD-ID}/PRD.md` to generate._

| ID | Title | Status | Plan | Branch |
|----|-------|--------|------|--------|

## Legend
- `todo` — not started
- `in-progress` — plan exists, work underway
- `in-review` — implementation done, awaiting review
- `done` — merged
- `blocked` — waiting on dependency
```

`index.md` is a derived view. Story files are the source of truth. Any command that mutates story status MUST regenerate `index.md`.

---

## Process

### Phase 1: EXTRACT
- Review conversation history
- Identify explicit requirements + implicit needs
- Note constraints/preferences
- If critical info missing, ask before generating. Wait for response.

### Phase 2: SYNTHESIZE
- Organize into sections, fill assumptions, ensure feasibility

### Phase 3: GENERATE
- Write PRD with frontmatter + sections
- Write initial `index.md`
- Use markdown, concrete examples, code snippets where useful

### Phase 4: VALIDATE
- All required sections present
- Frontmatter complete and valid YAML
- MVP scope realistic
- IDs unique and sequential

---

## Phase 5: OUTPUT

```markdown
## PRD Created

**ID**: {PRD-ID}
**Files**:
- `.agents/PRDs/{PRD-ID}/PRD.md`
- `.agents/PRDs/{PRD-ID}/index.md`

**Product**: {Name}
**Epic Branch**: `epic/{PRD-ID}-{slug}` (base: `{base_branch}`)

### Sections Summary
- {N} user stories outlined
- {N} MVP features in scope
- {N} implementation phases
- {N} risks identified

### Assumptions Made
{List or "None"}

### Recommended Next Steps
1. Review the PRD
2. Generate stories: `/create-stories .agents/PRDs/{PRD-ID}/PRD.md`
3. Plan first story: `/plan .agents/stories/{PRD-ID}/STORY-001-{slug}.md`
4. Implement: `/implement .agents/plans/{PRD-ID}/STORY-001-{slug}.plan.md`
```

---

## Style Guidelines

- Tone: professional, action-oriented
- Format: markdown (headings, lists, tables, checkboxes)
- Specificity: concrete > abstract
- Length: comprehensive but scannable
