import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pais import Pais
from app.repositories import pais as repo
from app.schemas.pais import PaisCreate, PaisRead, PaisUpdate

logger = logging.getLogger("api.services.pais")


def _check_nombre_unique(db: Session, nombre: str, exclude_id: int | None = None) -> None:
    existing = repo.get_by_nombre(db, nombre)
    if existing and existing.id != exclude_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"País con nombre '{nombre}' ya existe",
        )


def _check_codigo_unique(db: Session, codigo: str, exclude_id: int | None = None) -> None:
    existing = repo.get_by_codigo_iso(db, codigo)
    if existing and existing.id != exclude_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"País con código ISO '{codigo}' ya existe",
        )


def _get_or_404(db: Session, pais_id: int) -> Pais:
    pais = repo.get(db, pais_id)
    if not pais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"País con id {pais_id} no encontrado",
        )
    return pais


def get_pais(db: Session, pais_id: int) -> PaisRead:
    logger.debug("get_pais id=%d", pais_id)
    return PaisRead.model_validate(repo.get(db, pais_id) or _get_or_404(db, pais_id))


def list_paises(db: Session, skip: int = 0, limit: int = 100) -> list[PaisRead]:
    logger.debug("list_paises skip=%d limit=%d", skip, limit)
    return [PaisRead.model_validate(p) for p in repo.list_all(db, skip, limit)]


def create_pais(db: Session, data: PaisCreate) -> PaisRead:
    logger.info("create_pais nombre=%s codigo=%s", data.nombre, data.codigo_iso)
    _check_nombre_unique(db, data.nombre)
    _check_codigo_unique(db, data.codigo_iso)
    return PaisRead.model_validate(repo.create(db, data))


def update_pais(db: Session, pais_id: int, data: PaisUpdate) -> PaisRead:
    logger.info("update_pais id=%d", pais_id)
    pais = _get_or_404(db, pais_id)
    if data.nombre:
        _check_nombre_unique(db, data.nombre, exclude_id=pais_id)
    if data.codigo_iso:
        _check_codigo_unique(db, data.codigo_iso, exclude_id=pais_id)
    return PaisRead.model_validate(repo.update(db, pais, data))


def delete_pais(db: Session, pais_id: int) -> None:
    logger.info("delete_pais id=%d", pais_id)
    pais = _get_or_404(db, pais_id)
    repo.delete(db, pais)
