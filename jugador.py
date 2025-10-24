from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Jugador
from datetime import datetime

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])

@router.post("/")
def crear_jugador(jugador: Jugador, session: Session = Depends(get_session)):
    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador


@router.get("/")
def listar_jugadores(session: Session = Depends(get_session)):
    statement = select(Jugador).where(Jugador.activo == True)
    return session.exec(statement).all()


@router.get("/{jugador_id}")
def obtener_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador or not jugador.activo:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@router.get("/inactivos")
def listar_jugadores_inactivos(session: Session = Depends(get_session)):
    statement = select(Jugador).where(Jugador.activo == False)
    return session.exec(statement).all()


@router.patch("/{jugador_id}")
def actualizar_jugador(jugador_id: int, jugador: Jugador, session: Session = Depends(get_session)):
    db_jugador = session.get(Jugador, jugador_id)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    jugador_data = jugador.dict(exclude_unset=True)
    for key, value in jugador_data.items():
        setattr(db_jugador, key, value)

    session.commit()
    session.refresh(db_jugador)
    return db_jugador


@router.patch("/recuperar/{jugador_id}")
def recuperar_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    jugador.activo = True
    jugador.fecha_inactivacion = None

    session.commit()
    session.refresh(jugador)
    return {"ok": True, "mensaje": "Jugador restaurado correctamente"}


@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    jugador.activo = False
    jugador.fecha_inactivacion = datetime.now().isoformat()

    session.commit()
    session.refresh(jugador)
    return {"ok": True, "mensaje": "Jugador desactivado (soft delete)"}