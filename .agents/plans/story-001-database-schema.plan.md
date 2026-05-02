# Plan: STORY-001 Database Schema and Persistence (SQLite)

## Summary

Implement the database layer for chat sessions and message history using the established FastAPI + SQLAlchemy architecture. This includes defining ORM models, Pydantic schemas for data validation, and the repository pattern for data access.

## User Story

As a developer, I want to implement the SQLite database schema using SQLAlchemy so that we can persist chat sessions and message history locally.

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | Backend (models, schemas, repositories) |
| Jira Issue | STORY-001 |

---

## Patterns to Follow

### Naming
```python
// SOURCE: backend/app/models/pais.py:1-12
class Pais(Base):
    __tablename__ = "paises"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # ...
```

### Error Handling
```python
// SOURCE: backend/app/services/pais.py:27-34
def _get_or_404(db: Session, pais_id: int) -> Pais:
    pais = repo.get(db, pais_id)
    if not pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"País con id {pais_id} no encontrado",
        )
    return pais
```

### Repositories
```python
// SOURCE: backend/app/repositories/pais.py:1-40
def get(db: Session, pais_id: int) -> Pais | None:
    return db.get(Pais, pais_id)

def create(db: Session, data: PaisCreate) -> Pais:
    pais = Pais(**data.model_dump())
    db.add(pais)
    db.commit()
    db.refresh(pais)
    return pais
```

---

## Files to Change

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/models/session.py` | CREATE | Define the Session ORM model |
| `backend/app/models/message.py` | CREATE | Define the Message ORM model |
| `backend/app/schemas/session.py` | CREATE | Define Pydantic schemas for Session |
| `backend/app/schemas/message.py` | CREATE | Define Pydantic schemas for Message |
| `backend/app/repositories/session.py` | CREATE | Implement data access for Sessions |
| `backend/app/repositories/message.py` | CREATE | Implement data access for Messages |
| `backend/app/models/__init__.py` | UPDATE | Export models for discovery by Base.metadata |

---

## Tasks

### Task 1: Create Session and Message Models

- **File**: `backend/app/models/session.py`, `backend/app/models/message.py`
- **Action**: CREATE
- **Implement**: 
    - `Session`: `id`, `title`, `created_at`, `updated_at`. Relationship to `messages`.
    - `Message`: `id`, `session_id` (FK), `role`, `content`, `timestamp`. Relationship to `session`.
- **Mirror**: `backend/app/models/pais.py`
- **Validate**: `cd backend && python -c "from app.models.session import Session; from app.models.message import Message; print('OK')"`

### Task 2: Create Session and Message Schemas

- **File**: `backend/app/schemas/session.py`, `backend/app/schemas/message.py`
- **Action**: CREATE
- **Implement**: 
    - `SessionBase`, `SessionCreate`, `SessionUpdate`, `SessionRead`.
    - `MessageBase`, `MessageCreate`, `MessageRead`.
- **Mirror**: `backend/app/schemas/pais.py`
- **Validate**: `cd backend && python -c "from app.schemas.session import SessionRead; from app.schemas.message import MessageRead; print('OK')"`

### Task 3: Create Repositories

- **File**: `backend/app/repositories/session.py`, `backend/app/repositories/message.py`
- **Action**: CREATE
- **Implement**: 
    - `get`, `list_all`, `create`, `update`, `delete` for sessions.
    - `get`, `list_by_session`, `create`, `delete` for messages.
- **Mirror**: `backend/app/repositories/pais.py`
- **Validate**: `cd backend && python -c "from app.repositories import session as session_repo; from app.repositories import message as message_repo; print('OK')"`

### Task 4: Register Models in __init__

- **File**: `backend/app/models/__init__.py`
- **Action**: UPDATE
- **Implement**: Import `Session` and `Message` to ensure they are registered with SQLAlchemy's `Base`.
- **Validate**: `cd backend && python -c "from app.main import app; print('OK')"`

---

## Validation

```bash
# Backend smoke test (ensure no import errors)
cd backend && python -c "from app.main import app; print('OK')"
```

---

## Acceptance Criteria

- [ ] SQLAlchemy models created with correct fields and relationships.
- [ ] Pydantic schemas created for validation.
- [ ] Repository pattern implemented for basic CRUD.
- [ ] Models registered in `backend/app/models/__init__.py`.
- [ ] Backend application starts without error (tables will be auto-created by `Base.metadata.create_all`).
