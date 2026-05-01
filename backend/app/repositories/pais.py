from sqlalchemy.orm import Session

from app.models.pais import Pais
from app.schemas.pais import PaisCreate, PaisUpdate


def get(db: Session, pais_id: int) -> Pais | None:
    return db.get(Pais, pais_id)


def get_by_nombre(db: Session, nombre: str) -> Pais | None:
    return db.query(Pais).filter(Pais.nombre == nombre).first()


def get_by_codigo_iso(db: Session, codigo_iso: str) -> Pais | None:
    return db.query(Pais).filter(Pais.codigo_iso == codigo_iso).first()


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[Pais]:
    return db.query(Pais).offset(skip).limit(limit).all()


def create(db: Session, data: PaisCreate) -> Pais:
    pais = Pais(**data.model_dump())
    db.add(pais)
    db.commit()
    db.refresh(pais)
    return pais


def update(db: Session, pais: Pais, data: PaisUpdate) -> Pais:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pais, field, value)
    db.commit()
    db.refresh(pais)
    return pais


def delete(db: Session, pais: Pais) -> None:
    db.delete(pais)
    db.commit()
