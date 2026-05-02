# AGENTS.md

This file provides guidance to AI Agent when working with the backend codebase.

## Project Overview

FastAPI REST API template with SQLite + SQLAlchemy. Strict layered architecture separates HTTP concerns, business logic, and data access.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | HTTP framework, routing, dependency injection |
| Uvicorn | ASGI server |
| SQLAlchemy 2.x | ORM, session management |
| Pydantic v2 | Request/response schemas, validation |
| pydantic-settings | Config from `.env` |
| SQLite | Default dev database (`app.db`) |

---

## Commands

```bash
# Install
pip install -r requirements.txt

# Development (run from backend/)
uvicorn app.main:app --reload

# Validate
curl http://localhost:8000/health
```

---

## Architecture

```
backend/
├── app/
│   ├── main.py          # App factory, middleware, router registration
│   ├── core/
│   │   ├── config.py    # pydantic-settings (reads .env)
│   │   ├── database.py  # Engine, SessionLocal, Base, get_db()
│   │   └── middleware.py # LoggingMiddleware (request ID + timing)
│   ├── models/          # SQLAlchemy ORM models (extend Base)
│   ├── schemas/         # Pydantic schemas (Create / Update / Read)
│   ├── repositories/    # Raw DB queries, no business logic
│   ├── services/        # Business logic, raises HTTPException
│   └── routers/         # FastAPI routes, calls service layer only
├── .env                 # Local config (not committed)
├── .env.example         # Config template
└── requirements.txt
```

Data flow: `Router` → `Service` → `Repository` → `Model`

---

## Code Patterns

### Naming Conventions
- Files and variables: `snake_case`
- Classes (models, schemas): `PascalCase`
- Table names: `snake_case`, plural (`paises`)
- Schemas: `ResourceCreate`, `ResourceUpdate`, `ResourceRead`
- Loggers: `logging.getLogger("api.<layer>.<resource>")`

### File Organization
- One file per resource in each layer (`pais.py` in models, schemas, repos, services, routers)
- `core/` holds infrastructure only — no business logic
- Register every router in `main.py` under `/api/v1`

### Adding a new resource

Follow the `pais` pattern exactly:

1. `models/<resource>.py` — SQLAlchemy model extending `Base`
2. `schemas/<resource>.py` — `ResourceBase`, `ResourceCreate`, `ResourceUpdate`, `ResourceRead`
3. `repositories/<resource>.py` — pure DB functions, no HTTP concerns, returns `None` on not found
4. `services/<resource>.py` — business logic, uniqueness checks, raises `HTTPException`
5. `routers/<resource>.py` — thin router, logs each request, calls service only
6. `main.py` — `app.include_router(resource_router, prefix="/api/v1")`

### Schema pattern
```python
class ResourceBase(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        return v.strip()

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: str | None = None   # All fields Optional

class ResourceRead(ResourceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
```

### Error Handling
- Services raise `HTTPException` directly — no custom exception classes
- 404 via `_get_or_404()` helper in service layer
- 409 for uniqueness violations
- Repositories never raise HTTP exceptions — return `None` on not found

### Database
- `get_db()` yields session via `Depends()` — never instantiate `SessionLocal` in routes
- Tables auto-created on startup via `Base.metadata.create_all(bind=engine)`
- SQLite: `connect_args={"check_same_thread": False}` required
- Use `model_dump(exclude_unset=True)` in repo `update()` to avoid overwriting unset fields

### Config
- All settings read from `.env` via `app.core.config.settings`
- `ALLOWED_ORIGINS`: comma-separated string → `settings.origins_list` returns `list[str]`
- Never hardcode config values — always use `settings.*`

---

## Testing

No test suite configured. Validate endpoints manually:

```bash
curl http://localhost:8000/health
# Swagger UI
open http://localhost:8000/docs
# ReDoc
open http://localhost:8000/redoc
```

---

## Validation

```bash
uvicorn app.main:app --reload
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/<resource>
```

---

## Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | App entry point, middleware order matters |
| `app/core/config.py` | All env var definitions |
| `app/core/database.py` | `get_db` dependency, `Base` for all models |
| `app/models/Entity.py` | Reference ORM model |
| `app/schemas/Entity.py` | Reference schema set |
| `app/repositories/Entity.py` | Reference repository |
| `app/services/Entity.py` | Reference service with uniqueness guards |
| `app/routers/Entity.py` | Reference router implementation |
| `.env.example` | All required environment variables |

---

## Notes

- No Alembic — schema changes require manual DB deletion or migrate to Alembic
- API prefix: `/api/v1`
- Health check: `GET /health`
- Auto-docs: `GET /docs` (Swagger), `GET /redoc`
- `LoggingMiddleware` adds `X-Request-ID` header to every response
- Python 3.10+ required (uses `str | None` union syntax)
