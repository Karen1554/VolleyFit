from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Entrenador

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])


@router.post("/")
def crear_entrenador(entrenador: Entrenador, session: Session = Depends(get_session)):
    session.add(entrenador)
    session.commit()
    session.refresh(entrenador)
    return entrenador


@router.get("/")
def listar_entrenadores(session: Session = Depends(get_session)):
    return session.exec(select(Entrenador)).all()


@router.get("/{entrenador_id}")
def obtener_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador


@router.put("/{entrenador_id}")
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


@router.delete("/{entrenador_id}")
def eliminar_entrenador(entrenador_id: int, session: Session = Depends(get_session)):
    entrenador = session.get(Entrenador, entrenador_id)
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    session.delete(entrenador)
    session.commit()
    return {"ok": True}