from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Metrica
from datetime import datetime

router = APIRouter(prefix="/metricas", tags=["Metricas"])


@router.post("/")
def crear_metrica(metrica: Metrica, session: Session = Depends(get_session)):
    session.add(metrica)
    session.commit()
    session.refresh(metrica)
    return metrica


@router.get("/")
def listar_metricas(session: Session = Depends(get_session)):
    statement = select(Metrica).where(Metrica.activo == True)
    return session.exec(statement).all()


@router.get("/{metrica_id}")
def obtener_metrica(metrica_id: int, session: Session = Depends(get_session)):
    metrica = session.get(Metrica, metrica_id)
    if not metrica or not metrica.activo:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")
    return metrica


@router.get("/por_jugador/{jugador_id}")
def metricas_por_jugador(jugador_id: int, session: Session = Depends(get_session)):
    statement = select(Metrica).where((Metrica.jugador_id == jugador_id) & (Metrica.activo == True))
    return session.exec(statement).all()


@router.get("/por_entrenamiento/{entrenamiento_id}")
def metricas_por_entrenamiento(entrenamiento_id: int, session: Session = Depends(get_session)):
    statement = select(Metrica).where((Metrica.entrenamiento_id == entrenamiento_id) & (Metrica.activo == True))
    return session.exec(statement).all()


@router.get("/inactivas")
def listar_metricas_inactivas(session: Session = Depends(get_session)):
    statement = select(Metrica).where(Metrica.activo == False)
    return session.exec(statement).all()


@router.put("/{metrica_id}")
def actualizar_metrica(metrica_id: int, metrica: Metrica, session: Session = Depends(get_session)):
    db_metrica = session.get(Metrica, metrica_id)
    if not db_metrica:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")

    metrica_data = metrica.dict(exclude_unset=True)
    for key, value in metrica_data.items():
        setattr(db_metrica, key, value)

    session.add(db_metrica)
    session.commit()
    session.refresh(db_metrica)
    return db_metrica


@router.put("/recuperar/{metrica_id}")
def recuperar_metrica(metrica_id: int, session: Session = Depends(get_session)):
    metrica = session.get(Metrica, metrica_id)
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")
    metrica.activo = True
    metrica.fecha_inactivacion = None
    session.add(metrica)
    session.commit()
    session.refresh(metrica)
    return {"ok": True, "mensaje": "Métrica restaurada correctamente"}


@router.delete("/{metrica_id}")
def eliminar_metrica(metrica_id: int, session: Session = Depends(get_session)):
    metrica = session.get(Metrica, metrica_id)
    if not metrica:
        raise HTTPException(status_code=404, detail="Métrica no encontrada")
    metrica.activo = False
    metrica.fecha_inactivacion = datetime.now().isoformat()
    session.add(metrica)
    session.commit()
    session.refresh(metrica)
    return {"ok": True, "mensaje": "Métrica desactivada (soft delete)"}