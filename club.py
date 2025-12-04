from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from db import get_session
from models import Club
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/clubes", tags=["Clubes"])

# Modelos Pydantic para entrada/salida
class ClubCreate(BaseModel):
    nombre: str
    ciudad: str
    activo: bool = True
    logo_url: Optional[str] = None

class ClubUpdate(BaseModel):
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    activo: Optional[bool] = None
    logo_url: Optional[str] = None


@router.post("/crear", response_model=Club)
def crear_club(club_data: ClubCreate, session: Session = Depends(get_session)):
    club = Club(
        nombre=club_data.nombre,
        ciudad=club_data.ciudad,
        activo=club_data.activo,
        logo_url=club_data.logo_url
    )
    session.add(club)
    session.commit()
    session.refresh(club)
    return club


@router.get("/listar", response_model=list[Club])
def listar_clubes(session: Session = Depends(get_session)):
    clubes = session.exec(select(Club).where(Club.activo == True)).all()
    if not clubes:
        raise HTTPException(status_code=404, detail="No hay clubes registrados")
    return clubes


@router.get("/ver/{club_id}", response_model=Club)
def obtener_club(
    club_id: int = Path(..., title="ID del club", ge=1),
    session: Session = Depends(get_session)
):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return club


@router.patch("/actualizar/{club_id}", response_model=Club)
def actualizar_club(
    club_id: int = Path(..., title="ID del club a actualizar", ge=1),
    datos_actualizados: ClubUpdate = None,
    session: Session = Depends(get_session)
):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    if datos_actualizados.nombre is not None:
        club.nombre = datos_actualizados.nombre
    if datos_actualizados.ciudad is not None:
        club.ciudad = datos_actualizados.ciudad
    if datos_actualizados.activo is not None:
        club.activo = datos_actualizados.activo
    if datos_actualizados.logo_url is not None:
        club.logo_url = datos_actualizados.logo_url

    session.add(club)
    session.commit()
    session.refresh(club)
    return club



@router.delete("/eliminar/{club_id}")
def eliminar_club(
    club_id: int = Path(..., title="ID del club a eliminar", ge=1),
    session: Session = Depends(get_session)
):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    club.activo = False
    session.add(club)
    session.commit()
    return {"message": f"⚠️ Club '{club.nombre}' fue desactivado (soft delete)"}



@router.patch("/restaurar/{club_id}")
def restaurar_club(
    club_id: int = Path(..., title="ID del club a restaurar", ge=1),
    session: Session = Depends(get_session)
):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    club.activo = True
    session.add(club)
    session.commit()
    return {"message": f"✅ Club '{club.nombre}' fue restaurado correctamente"}
