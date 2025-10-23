from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import JugadorEntrenamiento

router = APIRouter(prefix="/jugador_entrenamientos", tags=["Jugador-Entrenamientos"])


@router.post("/")
def crear_relacion(relacion: JugadorEntrenamiento, session: Session = Depends(get_session)):
    session.add(relacion)
    session.commit()
    session.refresh(relacion)
    return relacion


@router.get("/")
def listar_relaciones(session: Session = Depends(get_session)):
    return session.exec(select(JugadorEntrenamiento)).all()


@router.get("/{relacion_id}")
def obtener_relacion(relacion_id: int, session: Session = Depends(get_session)):
    relacion = session.get(JugadorEntrenamiento, relacion_id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return relacion


@router.put("/{relacion_id}")
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


@router.delete("/{relacion_id}")
def eliminar_relacion(relacion_id: int, session: Session = Depends(get_session)):
    relacion = session.get(JugadorEntrenamiento, relacion_id)
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    session.delete(relacion)
    session.commit()
    return {"ok": True, "mensaje": "Relación eliminada correctamente"}
