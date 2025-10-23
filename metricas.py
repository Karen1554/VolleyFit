from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Metrica

router = APIRouter(prefix="/metricas", tags=["Metricas"])


@router.post("/")
def crear_metrica(metrica: Metrica, session: Session = Depends(get_session)):
    session.add(metrica)
    session.commit()
    session.refresh(metrica)
    return metrica


@router.get("/")
def listar_metricas(session: Session = Depends(get_session)):
    return session.exec(select(Metrica)).all()


@router.get("/{metrica_id}")
def obtener_metrica(metrica_id: int, session: Session = Depends(get_session)):
    metrica = session.get(Metrica, metrica_id)
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")
    return metrica


@router.get("/por_jugador/{jugador_id}")
def metricas_por_jugador(jugador_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Metrica).where(Metrica.jugador_id == jugador_id)).all()


@router.get("/por_entrenamiento/{entrenamiento_id}")
def metricas_por_entrenamiento(entrenamiento_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Metrica).where(Metrica.entrenamiento_id == entrenamiento_id)).all()


@router.put("/{metrica_id}")
def actualizar_metrica(metrica_id: int, metrica: Metrica, session: Session = Depends(get_session)):
    db_metrica = session.get(Metrica, metrica_id)
    if not db_metrica:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")

    metrica_data = metrica.dict(exclude_unset=True)
    for key, value in metrica_data.items():
        setattr(db_metrica, key, value)

    session.commit()
    session.refresh(db_metrica)
    return db_metrica


@router.delete("/{metrica_id}")
def eliminar_metrica(metrica_id: int, session: Session = Depends(get_session)):
    metrica = session.get(Metrica, metrica_id)
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")
    session.delete(metrica)
    session.commit()
    return {"ok": True, "mensaje": "Métrica eliminada correctamente"}
