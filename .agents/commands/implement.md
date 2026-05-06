---
description: Execute a story implementation plan, commit on epic branch
argument-hint: <path/to/plan.md>
---

# Implement Plan (local file workflow, single-branch per epic)

**Plan**: $ARGUMENTS

## Mission

Execute the plan end-to-end with rigorous self-validation. All work for a PRD lives on its single epic branch — no per-story branches. Each finished story = one commit on the epic branch. Update story status + regenerate PRD `index.md`. No Jira.

**Core Philosophy**: Validation loops catch mistakes early. Run checks after every change. Fix issues immediately.

**Golden Rule**: If validation fails, fix it before moving on. Never accumulate broken state.

---

## Phase 1: LOAD

### Read the Plan

Load plan file. Extract from frontmatter + body:

- `story` — story ID (e.g. `STORY-001`)
- `prd` — PRD ID (e.g. `PRD-001`)
- `epic_branch` — epic branch (e.g. `epic/PRD-001-user-auth`)
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
- PRD frontmatter at `.agents/PRDs/{prd}/PRD.md` (for `base_branch` + `epic_branch`)

---

## Phase 2: PREPARE GIT (epic branch only)

### 2.1 Inspect State

```bash
git branch --show-current
git status --short
```

| State | Action |
|-------|--------|
| Working tree dirty (unrelated changes) | STOP: "Stash or commit changes first" |
| Working tree clean | Proceed |

### 2.2 Ensure Epic Branch Exists + Switch to It

Read `base_branch` + `epic_branch` from PRD frontmatter.

```bash
# Does epic branch exist?
git rev-parse --verify {epic_branch} 2>/dev/null
```

| State | Action |
|-------|--------|
| Epic branch missing | `git checkout {base_branch} && git pull --ff-only && git checkout -b {epic_branch}` |
| Epic branch exists, not current | `git checkout {epic_branch}` |
| Already on epic branch | proceed |

**No story branch is created.** All story commits land directly on `{epic_branch}`.

### 2.3 Confirm Predecessors Committed

Story commits are sequential on the epic branch. If a previous story for this PRD is `in-review` or `done` but has no `commit` SHA in its frontmatter, warn the user — earlier work may be uncommitted on the same branch.

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

## Phase 5: COMMIT THE STORY

One commit per story on the epic branch.

### 5.1 Stage Files

Stage only files actually produced by this story (code + tests + .agents/ artifacts for this story):

```bash
git add <files-for-this-story>
```

Avoid `git add -A` / `git add .` to keep unrelated untracked files out of the commit.

### 5.2 Commit

Commit message format (Conventional Commits, reference the story):

```bash
git commit -m "$(cat <<'EOF'
<type>({scope}): <STORY-ID> <short summary>

<body explaining what was implemented and why, if non-obvious>

Story: {STORY-ID}
PRD: {PRD-ID}
Plan: .agents/plans/{PRD-ID}/completed/{STORY-ID}-{slug}.plan.md
Report: .agents/reports/{PRD-ID}/{STORY-ID}-{slug}.report.md

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

`<type>` examples: `feat`, `fix`, `refactor`, `chore`, `test`, `docs`.

### 5.3 Capture SHA

```bash
git rev-parse --short HEAD
```

Store the SHA — it goes into the story frontmatter and report.

---

## Phase 6: REPORT

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
epic_branch: {epic branch}
commit: {short SHA}
status: COMPLETE
completed: {YYYY-MM-DD}
---

# Implementation Report — {STORY-ID}: {Title}

**Plan**: `{plan-path}`
**Epic Branch**: `{epic branch}`
**Commit**: `{short SHA}`

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

If the report file or moved plan path was not part of the story commit, amend or follow up with a small chore commit. Prefer including them in the story commit when possible.

---

## Phase 7: UPDATE STORY + INDEX

### 7.1 Update Story File

Edit `.agents/stories/{PRD-ID}/{STORY-ID}-{slug}.md` frontmatter:
- `status: done`
- `commit: {short SHA}`
- `report: .agents/reports/{PRD-ID}/{STORY-ID}-{slug}.report.md`
- `plan: .agents/plans/{PRD-ID}/completed/{STORY-ID}-{slug}.plan.md`
- `updated: {YYYY-MM-DD}`

Status goes straight to `done` once committed on the epic branch. Reviews happen on the epic branch as a whole (or via the eventual PR from epic → base).

### 7.2 Regenerate Index

Rewrite `.agents/PRDs/{PRD-ID}/index.md` based on current story frontmatter (see `create-stories.md` Phase 5 for format). Show commit SHAs in the table.

Update PRD `updated` field.

These metadata updates can ride in the next story's commit, or be committed as a small chore commit (`chore({PRD-ID}): update {STORY-ID} status + index`).

---

## Phase 8: NEXT STEPS (manual epic merge)

Do NOT auto-merge. Surface clear commands.

```markdown
### Next Steps

1. Review report: `.agents/reports/{PRD-ID}/{STORY-ID}-{slug}.report.md`
2. Review diff for this commit: `git show {short SHA}`
3. Plan next story: `/plan <next-story-id>`
4. When all PRD stories are done, review the full epic vs base:
   ```bash
   git diff {base_branch}...{epic branch}
   git log --oneline {base_branch}..{epic branch}
   ```
5. Merge epic → `{base_branch}` when approved:
   ```bash
   git checkout {base_branch}
   git pull --ff-only
   git merge --no-ff {epic branch}
   git push
   ```
```

---

## Phase 9: OUTPUT

```markdown
## Implementation Complete

**Story**: {STORY-ID} — {title}
**PRD**: {PRD-ID}
**Epic Branch**: `{epic branch}`
**Commit**: `{short SHA}`
**Status**: ✅ done

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
- Story status: `todo` → `in-progress` → `done`
- Index updated: `.agents/PRDs/{PRD-ID}/index.md`

### Story Progress (PRD-level)

{done}/{total} stories done — {percent}%

### Next Steps

1. `/plan <next-story-id>` — continue on the same epic branch
2. When all stories done, merge epic → `{base_branch}` (commands above)
```

---

## Handling Failures

| Failure | Action |
|---------|--------|
| Type check fails | Read error, fix, re-run |
| Tests fail | Fix impl or test, re-run |
| Lint fails | `cd frontend && npm run lint`, fix manually |
| Backend import fails | Check Python syntax/imports, fix, re-run |
| Epic branch missing | Check `base_branch` exists; create epic from base |
| Dirty working tree (unrelated) | STOP, ask user to stash/commit |
| Commit hook fails | Fix underlying issue, stage fix, create NEW commit (do not amend the failed one blindly) |
