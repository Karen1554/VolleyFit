from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Jugador

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])


@router.post("/")
def crear_jugador(jugador: Jugador, session: Session = Depends(get_session)):
    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador


@router.get("/")
def listar_jugadores(session: Session = Depends(get_session)):
    return session.exec(select(Jugador)).all()


@router.get("/{jugador_id}")
def obtener_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@router.put("/{jugador_id}")
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


@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int, session: Session = Depends(get_session)):
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    session.delete(jugador)
    session.commit()
    return {"ok": True}
