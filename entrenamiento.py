from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Entrenamiento

router = APIRouter(prefix="/entrenamientos", tags=["Entrenamientos"])


@router.post("/")
def crear_entrenamiento(entrenamiento: Entrenamiento, session: Session = Depends(get_session)):
    session.add(entrenamiento)
    session.commit()
    session.refresh(entrenamiento)
    return entrenamiento


@router.get("/")
def listar_entrenamientos(session: Session = Depends(get_session)):
    return session.exec(select(Entrenamiento)).all()


@router.get("/{entrenamiento_id}")
def obtener_entrenamiento(entrenamiento_id: int, session: Session = Depends(get_session)):
    entrenamiento = session.get(Entrenamiento, entrenamiento_id)
    if not entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    return entrenamiento


@router.put("/{entrenamiento_id}")
def actualizar_entrenamiento(entrenamiento_id: int, entrenamiento: Entrenamiento, session: Session = Depends(get_session)):
    db_entrenamiento = session.get(Entrenamiento, entrenamiento_id)
    if not db_entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")

    entrenamiento_data = entrenamiento.dict(exclude_unset=True)
    for key, value in entrenamiento_data.items():
        setattr(db_entrenamiento, key, value)

    session.commit()
    session.refresh(db_entrenamiento)
    return db_entrenamiento


@router.delete("/{entrenamiento_id}")
def eliminar_entrenamiento(entrenamiento_id: int, session: Session = Depends(get_session)):
    entrenamiento = session.get(Entrenamiento, entrenamiento_id)
    if not entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    session.delete(entrenamiento)
    session.commit()
    return {"ok": True}
