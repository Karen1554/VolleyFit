from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Entrenador
from datetime import datetime

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])


@router.post("/")
def crear_entrenador(entrenador: Entrenador, session: Session = Depends(get_session)):
    session.add(entrenador)
    session.commit()
    session.refresh(entrenador)
    return entrenador


@router.get("/")
def listar_entrenadores(session: Session = Depends(get_session)):
    statement = select(Entrenador).where(Entrenador.activo == True)
    return session.exec(statement).all()


@router.get("/{entrenador_id}")
def obtener_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador or not entrenador.activo:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador


@router.get("/inactivos")
def listar_entrenadores_inactivos(session: Session = Depends(get_session)):
    statement = select(Entrenador).where(Entrenador.activo == False)
    return session.exec(statement).all()


@router.get("/por-club/{club_id}")
def listar_entrenadores_por_club(club_id: int, session: Session = Depends(get_session)):
    statement = select(Entrenador).where(Entrenador.club_id == club_id).where(Entrenador.activo == True)
    entrenadores = session.exec(statement).all()
    if not entrenadores:
        return []
    return entrenadores


@router.patch("/{entrenador_id}")
def actualizar_entrenador(entrenador_id: int, entrenador: Entrenador, session: Session = Depends(get_session)):
    db_entrenador = session.get(Entrenador, entrenador_id)
    if not db_entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador_data = entrenador.dict(exclude_unset=True)
    for key, value in entrenador_data.items():
        setattr(db_entrenador, key, value)

    session.commit()
    session.refresh(db_entrenador)
    return db_entrenador


@router.patch("/recuperar/{entrenador_id}")
def recuperar_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador.activo = True
    entrenador.fecha_inactivacion = None

    session.commit()
    session.refresh(entrenador)
    return {"ok": True, "mensaje": "Entrenador restaurado correctamente"}


@router.delete("/{entrenador_id}")
def eliminar_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")

    entrenador.activo = False
    entrenador.fecha_inactivacion = datetime.now().isoformat()

    session.commit()
    session.refresh(entrenador)
    return {"ok": True, "mensaje": "Entrenador desactivado (soft delete)"}