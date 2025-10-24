from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Entrenamiento
from datetime import datetime

router = APIRouter(prefix="/entrenamientos", tags=["Entrenamientos"])

@router.post("/")
def crear_relacion(relacion: JugadorEntrenamiento, session: Session = Depends(get_session)):
    session.add(relacion)
    session.commit()
    session.refresh(relacion)
    return relacion


@router.get("/")
def listar_relaciones(session: Session = Depends(get_session)):
    statement = select(JugadorEntrenamiento).where(JugadorEntrenamiento.activo == True)
    return session.exec(statement).all()


@router.get("/{relacion_id}")
def obtener_relacion(relacion_id: int, session: Session = Depends(get_session)):
    relacion = session.get(JugadorEntrenamiento, relacion_id)
    if not relacion or not relacion.activo:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return relacion


@router.get("/inactivos")
def listar_relaciones_inactivas(session: Session = Depends(get_session)):
    statement = select(JugadorEntrenamiento).where(JugadorEntrenamiento.activo == False)
    return session.exec(statement).all()


@router.patch("/{relacion_id}")
def actualizar_relacion(relacion_id: int, relacion: JugadorEntrenamiento, session: Session = Depends(get_session)):
    db_relacion = session.get(JugadorEntrenamiento, relacion_id)
    if not db_relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    relacion_data = relacion.dict(exclude_unset=True)
    for key, value in relacion_data.items():
        setattr(db_relacion, key, value)

    session.commit()
    session.refresh(db_relacion)
    return db_relacion


@router.patch("/recuperar/{relacion_id}")
def recuperar_relacion(relacion_id: int, session: Session = Depends(get_session)):
    relacion = session.get(JugadorEntrenamiento, relacion_id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    relacion.activo = True
    relacion.fecha_inactivacion = None

    session.commit()
    session.refresh(relacion)
    return {"ok": True, "mensaje": "Relación restaurada correctamente"}


@router.delete("/{relacion_id}")
def eliminar_relacion(relacion_id: int, session: Session = Depends(get_session)):
    relacion = session.get(JugadorEntrenamiento, relacion_id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    relacion.activo = False
    relacion.fecha_inactivacion = datetime.now().isoformat()

    session.commit()
    session.refresh(relacion)
    return {"ok": True, "mensaje": "Relación desactivada (soft delete)"}