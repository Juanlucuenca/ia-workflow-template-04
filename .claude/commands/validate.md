---
description: Run linter, type checker, and tests - report any failures
---

# Validate

Run all validation checks and report results.

---

## Checks to Run

### Frontend (run from `frontend/`)

```bash
# Lint (ESLint)
npm run lint
```

### Backend (run from `backend/`)

```bash
# Smoke test — verify API is up
curl http://localhost:8000/health
```

> No automated test suite yet. Validate backend by starting the server and hitting endpoints manually or with curl.

---

## Process

1. Run frontend lint from `frontend/`, capture output
2. Run backend smoke test if server is running
3. Collect all failures
4. Report results

---

## Output

Report in this format:

```
## Validation Results

| Check | Result | Details |
|-------|--------|---------|
| Frontend Lint | ✅/❌ | {N errors or "passed"} |
| Backend Health | ✅/❌ | {200 OK or error} |

### Summary
- **Status**: ✅ ALL PASSING / ❌ {N} FAILURES
- **Action needed**: {None / list of things to fix}
```

---

## If Failures Found

List each failure with:
1. File and line number
2. Error message
3. Suggested fix (if obvious)

Example:
```
### Failures

1. **frontend/src/components/Button.jsx:12**
   - Error: `'useState' is defined but never used`
   - Fix: Remove unused import

2. **backend/app/routers/items.py:45**
   - Error: Missing return type or logic error
   - Fix: Check function signature
```
