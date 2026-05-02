# AGENTS.md

This file provides guidance to AI Agent when working with this repository.

## Project Overview

Full-stack monorepo template: React 19 SPA frontend + FastAPI REST backend. Designed as a reusable starter for multi-page applications with a layered API. Frontend and backend are independent apps that communicate over HTTP.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 19 + Vite | SPA, component-based UI |
| Frontend | React Router 7 | Client-side routing (declarative mode) |
| Frontend | Tailwind CSS v4 + shadcn/ui | Styling + accessible components |
| Backend | FastAPI + Uvicorn | REST API, ASGI server |
| Backend | SQLAlchemy 2.x + SQLite | ORM + default dev database |
| Backend | Pydantic v2 | Schema validation |
| Config | pydantic-settings | Environment variable management |

---

## Commands

```bash
# Frontend (run from frontend/)
npm run dev        # Dev server — localhost:5173
npm run build      # Production build → dist/
npm run lint       # ESLint flat config
npm run preview    # Preview production build

# Backend (run from backend/)
pip install -r requirements.txt
uvicorn app.main:app --reload   # Dev server — localhost:8000
curl http://localhost:8000/health
```

---

## Architecture

```
ai-template-clase04/
├── frontend/       # React SPA (see frontend/AGENT.md)
├── backend/        # FastAPI REST API (see backend/AGENT.md)
├── .agents/        # Agent config, skills, commands
└── .agents/        # Agent-generated outputs (PRDs, stories)
```

Frontend and backend are fully decoupled. Run each independently. CORS is configured in `backend/app/core/config.py` via `ALLOWED_ORIGINS`.

---

## Code Patterns

### Cross-project conventions
- Frontend uses `@/` path alias for all imports
- Backend uses `snake_case` everywhere, `PascalCase` for classes
- Both projects log at module level with structured loggers

### Adding a new end-to-end feature
1. **Backend**: add resource following the `pais` pattern (model → schema → repo → service → router → register in `main.py`)
2. **Frontend**: add page in `src/pages/`, wire route in `src/App.jsx`, add nav link if needed
3. **API base URL**: configure in frontend via env var or constants file

---

## Testing

- No test suite configured yet in either project
- Backend: validate endpoints with `curl` or Swagger UI (`GET /docs`)
- Frontend: validate in browser via `npm run dev`

---

## Validation

```bash
# Frontend
cd frontend && npm run lint && npm run build

# Backend
cd backend && uvicorn app.main:app --reload
# then: curl http://localhost:8000/health
```

---

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/App.jsx` | All route definitions |
| `frontend/src/layouts/RootLayout.jsx` | App-wide layout shell |
| `backend/app/main.py` | FastAPI app factory, middleware, router registration |
| `backend/app/core/config.py` | All environment variables |
| `backend/app/core/database.py` | DB engine, session, `Base` |
| `backend/.env.example` | Required environment variables |

---

## On-Demand Context

| Topic | File |
|-------|------|
| Frontend patterns, routing, components | `frontend/AGENT.md` |
| Backend architecture, resource pattern | `backend/AGENT.md` |
| Skill definitions | `.agents/commands/` |

---

## Notes

- No Docker or shared dev runner — start frontend and backend separately
- No monorepo package manager (no workspaces) — each app manages its own deps
- CORS: set `ALLOWED_ORIGINS=http://localhost:5173` in `backend/.env` for local dev
- API prefix: `/api/v1` — all backend resource routes live under this prefix
