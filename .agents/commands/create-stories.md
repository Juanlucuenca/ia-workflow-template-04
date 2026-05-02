---
description: Generate local user story files from a PRD
argument-hint: <path-to-PRD.md | PRD-ID>
---

# Create Stories from PRD (local file workflow)

Generate one markdown file per user story under `.agents/stories/{PRD-ID}/`. Each story carries frontmatter the agent uses to track status across the workflow. No Jira.

**Input**: $ARGUMENTS

---

## Phase 1: LOAD

Resolve the PRD:
1. If arg is a file path → read directly.
2. If arg matches `PRD-NNN` → resolve to `.agents/PRDs/PRD-NNN-*/PRD.md`.
3. If arg blank → list `.agents/PRDs/` and ask which PRD.

Extract from PRD frontmatter:
- `id` (e.g. `PRD-001`)
- `slug`
- `base_branch`
- `epic_branch`

Extract from PRD body:
- User stories already defined
- Acceptance criteria from success criteria + requirements
- Implementation phases and deliverables
- Technical constraints and dependencies

---

## Phase 2: ANALYZE

### Break Down into Stories

For each feature/requirement:

1. **Story format**: `As a [user], I want [action], so that [benefit]`
2. **Acceptance criteria** (3-5 per story): `Given [context], when [action], then [result]`
3. **Complexity**: Small / Medium / Large
4. **Dependencies**: list blocking story IDs

### Categories

- `feature` — new functionality
- `enhancement` — improvement
- `bug` — fix
- `technical` — infra/refactor/tooling
- `spike` — research

---

## Phase 3: ASSIGN IDs

1. Story ID format: `STORY-{NNN}-{kebab-slug}` (NNN zero-pad 3, scoped per PRD).
2. Number sequentially starting at `001`. Order by phase, then dependencies (blockers before blocked), then priority.
3. Story directory: `.agents/stories/{PRD-ID}/`

```bash
mkdir -p .agents/stories/{PRD-ID}
```

---

## Phase 4: GENERATE STORY FILES

Write one file per story at `.agents/stories/{PRD-ID}/STORY-{NNN}-{slug}.md`:

```markdown
---
id: STORY-{NNN}
prd: {PRD-ID}
slug: {kebab-slug}
title: {Story title}
type: feature              # feature | enhancement | bug | technical | spike
priority: high             # high | medium | low
complexity: small          # small | medium | large
phase: {phase number/name from PRD}
status: todo               # todo | in-progress | in-review | done | blocked
labels: [backend, api]
branch: feature/{PRD-ID}/STORY-{NNN}-{slug}
base_branch: {epic_branch from PRD}
plan: null                 # filled when /plan runs
report: null               # filled when /implement completes
depends_on: []             # list of STORY-NNN IDs
blocks: []                 # list of STORY-NNN IDs
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# {STORY-ID}: {Title}

## Description

As a {user type}, I want to {action}, so that {benefit}.

## Acceptance Criteria

- [ ] Given {context}, when {action}, then {result}
- [ ] Given {context}, when {action}, then {result}
- [ ] Given {context}, when {action}, then {result}

## Technical Notes

- Key implementation details
- Files likely to be modified
- Patterns to follow (reference AGENTS.md or project conventions)

## Dependencies

- **Blocked by**: {STORY-IDs or "None"}
- **Blocks**: {STORY-IDs or "None"}

## PRD Reference

Source: [`{PRD-ID}/PRD.md`](../../PRDs/{PRD-ID}/PRD.md) — section {N}
```

---

## Phase 5: REGENERATE index.md

Rewrite `.agents/PRDs/{PRD-ID}/index.md` to reflect all stories.

Build the story table by reading every `*.md` file under `.agents/stories/{PRD-ID}/` and extracting frontmatter:

```markdown
# {PRD-ID}: {Title} — Story Board

**PRD**: [PRD.md](./PRD.md)
**Epic Branch**: `{epic_branch}` (base: `{base_branch}`)
**Status**: {derived: active if any story not done, else done}

## Progress

{count_done}/{count_total} stories done — {percent}%

## Stories

| ID | Title | Type | Status | Complexity | Plan | Branch |
|----|-------|------|--------|------------|------|--------|
| STORY-001 | {title} | feature | ⬜ todo | small | — | `feature/{PRD-ID}/STORY-001-{slug}` |
| STORY-002 | {title} | technical | 🟡 in-progress | medium | [plan](../../plans/{PRD-ID}/STORY-002-{slug}.plan.md) | `feature/{PRD-ID}/STORY-002-{slug}` |

## Status Icons
- ⬜ todo
- 🟡 in-progress
- 🔵 in-review
- ✅ done
- 🔴 blocked

## Dependencies

- STORY-002 blocked by STORY-001
- ...
```

Status icon mapping (use exactly):
- `todo` → ⬜
- `in-progress` → 🟡
- `in-review` → 🔵
- `done` → ✅
- `blocked` → 🔴

---

## Phase 6: VALIDATE

- [ ] Every PRD requirement maps to ≥1 story
- [ ] No story too large (split if >1-2 days work)
- [ ] Acceptance criteria testable and specific
- [ ] Dependencies form a DAG (no cycles)
- [ ] Stories cover full SDLC (types, validation, services, routes, UI, tests)
- [ ] Each story independently reviewable/mergeable
- [ ] All frontmatter fields populated
- [ ] `index.md` regenerated

---

## Phase 7: OUTPUT

```markdown
## Stories Created

**PRD**: {PRD-ID}
**Count**: {N} stories
**Directory**: `.agents/stories/{PRD-ID}/`

| ID | Title | Type | Complexity |
|----|-------|------|------------|
| STORY-001 | {title} | feature | small |
| ... | ... | ... | ... |

**Status Board**: `.agents/PRDs/{PRD-ID}/index.md`

### Next Steps
1. Review stories — adjust acceptance criteria as needed
2. Plan first story: `/plan .agents/stories/{PRD-ID}/STORY-001-{slug}.md`
```

---

## Tips

- Keep stories small (1-2 days max)
- Acceptance criteria must be verifiable without asking the author
- Technical stories also need acceptance criteria (build passes, tests pass)
- Reference PRD section in each story for traceability
- When status changes anywhere in the workflow, regenerate `index.md`
