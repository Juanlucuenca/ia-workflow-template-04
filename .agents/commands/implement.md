---
description: Execute a story implementation plan with branching + status updates
argument-hint: <path/to/plan.md>
---

# Implement Plan (local file workflow)

**Plan**: $ARGUMENTS

## Mission

Execute the plan end-to-end with rigorous self-validation. Manage git branches per PRD/story. Update story status + regenerate PRD `index.md`. No Jira.

**Core Philosophy**: Validation loops catch mistakes early. Run checks after every change. Fix issues immediately.

**Golden Rule**: If validation fails, fix it before moving on. Never accumulate broken state.

---

## Phase 1: LOAD

### Read the Plan

Load plan file. Extract from frontmatter + body:

- `story` — story ID (e.g. `STORY-001`)
- `prd` — PRD ID (e.g. `PRD-001`)
- `branch` — feature branch (e.g. `feature/PRD-001/STORY-001-login-form`)
- `base_branch` — epic branch (e.g. `epic/PRD-001-user-auth`)
- **Patterns to Mirror** — code to copy from
- **Files to Change** — CREATE/UPDATE list
- **Tasks** — implementation order
- **E2E Tests** — verification steps
- **Validation Commands** — how to verify

**If plan not found:**
```
Error: Plan not found at $ARGUMENTS
Create a plan first: /plan <story-id-or-path>
```

Also load:
- Story file at `.agents/stories/{prd}/{story}-{slug}.md` (for ACs, status check)
- PRD frontmatter at `.agents/PRDs/{prd}/PRD.md` (for `base_branch` of epic)

---

## Phase 2: PREPARE GIT

### 2.1 Inspect State

```bash
git branch --show-current
git status --short
```

| State | Action |
|-------|--------|
| Working tree dirty | STOP: "Stash or commit changes first" |
| Working tree clean | Proceed |

### 2.2 Ensure Epic Branch Exists

Read PRD's `base_branch` and `epic_branch`.

```bash
# Does epic branch exist?
git rev-parse --verify {epic_branch} 2>/dev/null
```

If absent:
```bash
git checkout {base_branch}
git pull --ff-only          # if remote tracked
git checkout -b {epic_branch}
```

If present, skip creation.

### 2.3 Create / Switch Story Branch

```bash
# Story branch from epic
git rev-parse --verify {feature_branch} 2>/dev/null
```

| State | Action |
|-------|--------|
| Story branch missing | `git checkout {epic_branch} && git checkout -b {feature_branch}` |
| Story branch exists, not current | `git checkout {feature_branch}` |
| Already on story branch | proceed |

---

## Phase 3: EXECUTE

For each task in the plan:

### 3.1 Verify Assumptions

Before writing code:
- Read the target file
- Read adjacent files (imports, importers)
- Verify plan's references — do referenced functions/interfaces/endpoints actually exist?
- If assumptions wrong, adapt before implementing. Document deviations.

### 3.2 Implement

- Read MIRROR file reference, understand pattern
- Make change as specified
- Check integration: imports resolve? Callers/callees still work? Data flow correct across boundaries?

### 3.3 Validate Immediately

Backend changes:
```bash
cd backend && python -c "from app.main import app; print('OK')"
```

Frontend changes:
```bash
cd frontend && npm run lint
```

If fails: read error → fix → re-run → only proceed when passing.

### 3.4 Track Progress

```
Task 1: CREATE src/x.ts ✅
Task 2: UPDATE src/y.ts ✅
```

Document deviations from plan with rationale.

---

## Phase 4: VALIDATE

### Run All Checks

```bash
cd frontend && npm run lint
cd backend && python -c "from app.main import app; print('OK')"
curl http://localhost:8000/health
```

All must pass with zero errors.

### Write Tests

You MUST write tests for new code:
- Every new function needs ≥1 test
- Error/edge cases need tests
- Update existing tests if behavior changed
- Test across boundaries (endpoint shape + data, not just isolated functions)

If tests fail: bug in impl or test? Fix actual issue. Re-run until green.

### REQUIRED: End-to-End Verification

> **⚠️ Do NOT proceed to Phase 5 until all E2E steps pass.**

Re-read plan's E2E section. Execute every test as a checklist:

- [ ] Start app (dev servers, DBs, etc.)
- [ ] For EACH E2E test in the plan:
  - [ ] Execute exactly as described
  - [ ] Verify outcome matches plan
  - [ ] If fails: fix → re-run → confirm passes
- [ ] Confirm all E2E tests pass

If plan has no E2E tests, perform basic smoke test (start app, exercise feature manually).

**Hard gate.** Cannot report complete until E2E passes.

---

## Phase 5: REPORT

### Create Report

**Path**: `.agents/reports/{PRD-ID}/{STORY-ID}-{slug}.report.md`

```bash
mkdir -p .agents/reports/{PRD-ID}
```

```markdown
---
story: {STORY-ID}
prd: {PRD-ID}
plan: {plan path}
branch: {feature branch}
base_branch: {epic branch}
status: COMPLETE
completed: {YYYY-MM-DD}
---

# Implementation Report — {STORY-ID}: {Title}

**Plan**: `{plan-path}`
**Branch**: `{feature branch}` (from `{epic branch}`)

## Summary

{Brief description of what was implemented}

## Tasks Completed

| # | Task | File | Status |
|---|------|------|--------|
| 1 | {description} | `src/x.ts` | ✅ |
| 2 | {description} | `src/y.ts` | ✅ |

## Validation Results

| Check | Result |
|-------|--------|
| Backend import | ✅ |
| Frontend lint | ✅ |
| Tests | ✅ ({N} passed) |
| E2E | ✅ ({N}/{N}) |

## Files Changed

| File | Action | Lines |
|------|--------|-------|
| `src/x.ts` | CREATE | +{N} |
| `src/y.ts` | UPDATE | +{N}/-{M} |

## Deviations from Plan

{List or "None"}

## Tests Written

| Test File | Test Cases |
|-----------|------------|
| `src/x.test.ts` | {list} |

## Acceptance Criteria

- [x] {AC 1}
- [x] {AC 2}
- [x] {AC N}
```

### Archive Plan

```bash
mkdir -p .agents/plans/{PRD-ID}/completed
mv {plan path} .agents/plans/{PRD-ID}/completed/
```

---

## Phase 6: UPDATE STORY + INDEX

### 6.1 Update Story File

Edit `.agents/stories/{PRD-ID}/{STORY-ID}-{slug}.md` frontmatter:
- `status: in-review`
- `report: .agents/reports/{PRD-ID}/{STORY-ID}-{slug}.report.md`
- `plan: .agents/plans/{PRD-ID}/completed/{STORY-ID}-{slug}.plan.md`
- `updated: {YYYY-MM-DD}`

### 6.2 Regenerate Index

Rewrite `.agents/PRDs/{PRD-ID}/index.md` based on current story frontmatter (see `create-stories.md` Phase 5 for format).

Update PRD `updated` field.

---

## Phase 7: MERGE GUIDANCE (manual)

Do NOT auto-merge. Surface clear next-step commands so the user can decide.

```markdown
### Next Steps

1. Review report: `.agents/reports/{PRD-ID}/{STORY-ID}-{slug}.report.md`
2. Review diff: `git diff {epic branch}...{feature branch}`
3. When approved, merge story → epic:
   ```bash
   git checkout {epic branch}
   git merge --no-ff {feature branch}
   ```
4. After merge, mark story `done` in `.agents/stories/{PRD-ID}/{STORY-ID}-{slug}.md` and regenerate `index.md`.
5. When all stories done, merge epic → `{base_branch}`:
   ```bash
   git checkout {base_branch}
   git merge --no-ff {epic branch}
   ```
```

---

## Phase 8: OUTPUT

```markdown
## Implementation Complete

**Story**: {STORY-ID} — {title}
**PRD**: {PRD-ID}
**Branch**: `{feature branch}` (from `{epic branch}`)
**Status**: ✅ in-review

### Validation

| Check | Result |
|-------|--------|
| Backend import | ✅ |
| Frontend lint | ✅ |
| Tests | ✅ |
| E2E | ✅ |

### Files Changed

- {N} files created
- {M} files updated
- {K} tests written

### Deviations

{Summary or "Implementation matched the plan."}

### Artifacts

- Report: `.agents/reports/{PRD-ID}/{STORY-ID}-{slug}.report.md`
- Plan archived: `.agents/plans/{PRD-ID}/completed/`
- Story status: `todo` → `in-progress` → `in-review`
- Index updated: `.agents/PRDs/{PRD-ID}/index.md`

### Story Progress (PRD-level)

{done}/{total} stories done — {percent}%

### Next Steps

1. Review diff: `git diff {epic branch}...{feature branch}`
2. Merge to epic when approved (commands above)
3. Mark story `done` after merge
4. Plan next story: `/plan <next-story-id>`
```

---

## Handling Failures

| Failure | Action |
|---------|--------|
| Type check fails | Read error, fix, re-run |
| Tests fail | Fix impl or test, re-run |
| Lint fails | `cd frontend && npm run lint`, fix manually |
| Backend import fails | Check Python syntax/imports, fix, re-run |
| Branch creation fails | Check `base_branch`/`epic_branch` exist, working tree clean |
| Dirty working tree | STOP, ask user to stash/commit |
