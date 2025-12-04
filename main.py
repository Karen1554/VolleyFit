from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import create_db_and_tables
import club
import entrenador
import jugador
import entrenamiento
import jugador_entrenamientos
import metricas

app = FastAPI(title="VolleyFit API", version="1.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(club.router)
app.include_router(entrenador.router)
app.include_router(jugador.router)
app.include_router(entrenamiento.router)
app.include_router(jugador_entrenamientos.router)
app.include_router(metricas.router)


@app.get("/")
def root():
    return {"message": "Bienvenido a VolleyFit API 🚀"}
