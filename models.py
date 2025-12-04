from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class JugadorEntrenamiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: int = Field(foreign_key="jugador.id")
    entrenamiento_id: int = Field(foreign_key="entrenamiento.id")


class Club(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    ciudad: str
    activo: bool
    logo_url: Optional[str] = None
    jugadores: List["Jugador"] = Relationship(back_populates="club")
    entrenadores: List["Entrenador"] = Relationship(back_populates="club")


class Entrenador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    experiencia: int
    especialidad: str
    activo: bool = True
    club_id: Optional[int] = Field(default=None, foreign_key="club.id")

    club: Optional[Club] = Relationship(back_populates="entrenadores")
    entrenamientos: List["Entrenamiento"] = Relationship(back_populates="entrenador")


class Jugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    posicion: str
    nivel: str
    club_id: Optional[int] = Field(default=None, foreign_key="club.id")

    club: Optional[Club] = Relationship(back_populates="jugadores")
    entrenamientos: List["Entrenamiento"] = Relationship(
        back_populates="jugadores", link_model=JugadorEntrenamiento
    )


class Entrenamiento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str
    duracion_minutos: int
    fecha: str
    descripcion: Optional[str] = None
    entrenador_id: Optional[int] = Field(default=None, foreign_key="entrenador.id")

    entrenador: Optional[Entrenador] = Relationship(back_populates="entrenamientos")
    jugadores: List[Jugador] = Relationship(
        back_populates="entrenamientos", link_model=JugadorEntrenamiento
    )



class Metrica(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: int = Field(foreign_key="jugador.id")
    entrenamiento_id: Optional[int] = Field(default=None, foreign_key="entrenamiento.id")
    salto: Optional[float] = None
    resistencia: Optional[float] = None
    recepcion: Optional[float] = None
