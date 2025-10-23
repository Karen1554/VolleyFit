from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Entrenamiento
from datetime import datetime

router = APIRouter(prefix="/entrenamientos", tags=["Entrenamientos"])


@router.post("/")
def crear_entrenamiento(entrenamiento: Entrenamiento, session: Session = Depends(get_session)):
    session.add(entrenamiento)
    session.commit()
    session.refresh(entrenamiento)
    return entrenamiento


@router.get("/")
def listar_entrenamientos(session: Session = Depends(get_session)):
    statement = select(Entrenamiento).where(Entrenamiento.activo == True)
    return session.exec(statement).all()


@router.get("/{entrenamiento_id}")
def obtener_entrenamiento(entrenamiento_id: int, session: Session = Depends(get_session)):
    entrenamiento = session.get(Entrenamiento, entrenamiento_id)
    if not entrenamiento or not entrenamiento.activo:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    return entrenamiento


@router.get("/inactivos")
def listar_entrenamientos_inactivos(session: Session = Depends(get_session)):
    statement = select(Entrenamiento).where(Entrenamiento.activo == False)
    return session.exec(statement).all()


@router.put("/{entrenamiento_id}")
def actualizar_entrenamiento(entrenamiento_id: int, entrenamiento: Entrenamiento, session: Session = Depends(get_session)):
    db_entrenamiento = session.get(Entrenamiento, entrenamiento_id)
    if not db_entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")

    entrenamiento_data = entrenamiento.dict(exclude_unset=True)
    for key, value in entrenamiento_data.items():
        setattr(db_entrenamiento, key, value)

    session.add(db_entrenamiento)
    session.commit()
    session.refresh(db_entrenamiento)
    return db_entrenamiento


@router.put("/recuperar/{entrenamiento_id}")
def recuperar_entrenamiento(entrenamiento_id: int, session: Session = Depends(get_session)):
    entrenamiento = session.get(Entrenamiento, entrenamiento_id)
    if not entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    entrenamiento.activo = True
    entrenamiento.fecha_inactivacion = None
    session.add(entrenamiento)
    session.commit()
    session.refresh(entrenamiento)
    return {"ok": True, "mensaje": "Entrenamiento restaurado correctamente"}


@router.delete("/{entrenamiento_id}")
def eliminar_entrenamiento(entrenamiento_id: int, session: Session = Depends(get_session)):
    entrenamiento = session.get(Entrenamiento, entrenamiento_id)
    if not entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    entrenamiento.activo = False
    entrenamiento.fecha_inactivacion = datetime.now().isoformat()
    session.add(entrenamiento)
    session.commit()
    session.refresh(entrenamiento)
    return {"ok": True, "mensaje": "Entrenamiento desactivado (soft delete)"}