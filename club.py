from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_session
from models import Club

router = APIRouter(prefix="/clubes", tags=["Clubes"])


@router.post("/")
def crear_club(club: Club, session: Session = Depends(get_session)):
    session.add(club)
    session.commit()
    session.refresh(club)
    return club


@router.get("/")
def listar_clubes(session: Session = Depends(get_session)):
    return session.exec(select(Club)).all()


@router.get("/{club_id}")
def obtener_club(club_id: int, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return club


@router.put("/{club_id}")
def actualizar_club(club_id: int, club: Club, session: Session = Depends(get_session)):
    db_club = session.get(Club, club_id)
    if not db_club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    club_data = club.dict(exclude_unset=True)
    for key, value in club_data.items():
        setattr(db_club, key, value)

    session.commit()
    session.refresh(db_club)
    return db_club


@router.delete("/{club_id}")
def eliminar_club(club_id: int, session: Session = Depends(get_session)):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    session.delete(club)
    session.commit()
    return {"ok": True}
