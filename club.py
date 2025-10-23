from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Club
from datetime import datetime

router = APIRouter(prefix="/clubes", tags=["Clubes"])


@router.post("/")
def crear_club(club: Club, session: Session = Depends(get_session)):
    session.add(club)
    session.commit()
    session.refresh(club)
    return club


@router.get("/")
def listar_clubes(session: Session = Depends(get_session)):
    statement = select(Club).where(Club.activo == True)
    return session.exec(statement).all()


@router.get("/{club_id}")
def obtener_club(club_id: int, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club or not club.activo:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return club


@router.get("/inactivos")
def listar_clubes_inactivos(session: Session = Depends(get_session)):
    statement = select(Club).where(Club.activo == False)
    return session.exec(statement).all()


@router.put("/{club_id}")
def actualizar_club(club_id: int, club: Club, session: Session = Depends(get_session)):
    db_club = session.get(Club, club_id)
    if not db_club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    club_data = club.dict(exclude_unset=True)
    for key, value in club_data.items():
        setattr(db_club, key, value)

    session.add(db_club)
    session.commit()
    session.refresh(db_club)
    return db_club


@router.put("/recuperar/{club_id}")
def recuperar_club(club_id: int, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    club.activo = True
    club.fecha_inactivacion = None
    session.add(club)
    session.commit()
    session.refresh(club)
    return {"ok": True, "mensaje": "Club restaurado correctamente"}


@router.delete("/{club_id}")
def eliminar_club(club_id: int, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    club.activo = False
    club.fecha_inactivacion = datetime.now().isoformat()
    session.add(club)
    session.commit()
    session.refresh(club)
    return {"ok": True, "mensaje": "Club desactivado (soft delete)"}