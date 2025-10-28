from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from db import get_session
from models import Club

router = APIRouter(prefix="/clubes", tags=["Clubes"])


# ➕ Crear un club
@router.post("/crear", response_model=Club)
def crear_club(club: Club, session: Session = Depends(get_session)):
    session.add(club)
    session.commit()
    session.refresh(club)
    return club


# 📋 Listar todos los clubes activos
@router.get("/listar", response_model=list[Club])
def listar_clubes(session: Session = Depends(get_session)):
    clubes = session.exec(select(Club).where(Club.activo == True)).all()
    if not clubes:
        raise HTTPException(status_code=404, detail="No hay clubes registrados")
    return clubes


# 🔍 Obtener un club por ID
@router.get("/ver/{club_id}", response_model=Club)
def obtener_club(
    club_id: int = Path(..., title="ID del club", ge=1),
    session: Session = Depends(get_session)
):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")
    return club


# 🧩 Actualizar parcialmente un club (PATCH)
@router.patch("/actualizar/{club_id}", response_model=Club)
def actualizar_club(
    club_id: int = Path(..., title="ID del club a actualizar", ge=1),
    datos_actualizados: Club = None,
    session: Session = Depends(get_session)
):
    club = session.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club no encontrado")

    # Solo actualiza los campos enviados
    if datos_actualizados.nombre:
        club.nombre = datos_actualizados.nombre
    if hasattr(datos_actualizados, "ciudad") and datos_actualizados.ciudad:
        club.ciudad = datos_actualizados.ciudad
    if hasattr(datos_actualizados, "categoria") and datos_actualizados.categoria:
        club.categoria = datos_actualizados.categoria

    session.add(club)
    session.commit()
    session.refresh(club)
    return club


# ❌ "Eliminar" (soft delete: marca como inactivo)
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


# ♻️ Restaurar un club desactivado
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
