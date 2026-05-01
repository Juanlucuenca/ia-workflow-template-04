import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.pais import PaisCreate, PaisRead, PaisUpdate
from app.services import pais as svc

logger = logging.getLogger("api.routers.pais")

router = APIRouter(prefix="/paises", tags=["paises"])


@router.get("/", response_model=list[PaisRead])
def list_paises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("GET /paises skip=%d limit=%d", skip, limit)
    return svc.list_paises(db, skip, limit)


@router.get("/{pais_id}", response_model=PaisRead)
def get_pais(pais_id: int, db: Session = Depends(get_db)):
    logger.info("GET /paises/%d", pais_id)
    return svc.get_pais(db, pais_id)


@router.post("/", response_model=PaisRead, status_code=status.HTTP_201_CREATED)
def create_pais(data: PaisCreate, db: Session = Depends(get_db)):
    logger.info("POST /paises nombre=%s", data.nombre)
    return svc.create_pais(db, data)


@router.put("/{pais_id}", response_model=PaisRead)
def update_pais(pais_id: int, data: PaisUpdate, db: Session = Depends(get_db)):
    logger.info("PUT /paises/%d", pais_id)
    return svc.update_pais(db, pais_id, data)


@router.delete("/{pais_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pais(pais_id: int, db: Session = Depends(get_db)):
    logger.info("DELETE /paises/%d", pais_id)
    svc.delete_pais(db, pais_id)
