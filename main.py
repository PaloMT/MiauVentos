import csv
from datetime import datetime, time
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambia "*" por tu dominio
    allow_methods=["*"],
    allow_headers=["*"],
)


def leer_eventos_csv():
    with open("eventos.csv", mode="r", encoding="utf-8") as archivo:
        # Cambia delimiter a ';' si el CSV viene de Excel en español
        return list(csv.DictReader(archivo, delimiter=","))


def a_numero(valor: str) -> Optional[float]:
    """Convierte '12,50' o '12.50' a float. Devuelve None si no es válido."""
    try:
        return float(valor.strip().replace(",", "."))
    except (ValueError, AttributeError):
        return None


def a_hora(valor: str) -> Optional[time]:
    """Convierte 'HH:MM' a time. Devuelve None si no es válido."""
    try:
        return datetime.strptime(valor.strip(), "%H:%M").time()
    except (ValueError, AttributeError):
        return None


@app.get("/api/eventos")
def obtener_eventos(
    categoria: Optional[str] = None,
    duracion_min: Optional[int] = Query(None, ge=0, description="Minutos"),
    duracion_max: Optional[int] = Query(None, ge=0, description="Minutos"),
    inicio_desde: Optional[str] = Query(None, pattern=r"^\d{2}:\d{2}$", description="HH:MM"),
    inicio_hasta: Optional[str] = Query(None, pattern=r"^\d{2}:\d{2}$", description="HH:MM"),
    precio_min: Optional[float] = Query(None, ge=0),
    precio_max: Optional[float] = Query(None, ge=0),
):
    desde = a_hora(inicio_desde) if inicio_desde else None
    hasta = a_hora(inicio_hasta) if inicio_hasta else None

    resultados = []

    for evento in leer_eventos_csv():
        # Categoría (parcial, sin distinguir mayúsculas)
        if categoria and categoria.lower() not in evento["categoria"].lower():
            continue

        # Duración
        if duracion_min is not None or duracion_max is not None:
            duracion = a_numero(evento["duracion"])
            if duracion is None:
                continue
            if duracion_min is not None and duracion < duracion_min:
                continue
            if duracion_max is not None and duracion > duracion_max:
                continue

        # Hora de inicio
        if desde or hasta:
            inicio = a_hora(evento["hora_inicio"])
            if inicio is None:
                continue
            if desde and inicio < desde:
                continue
            if hasta and inicio > hasta:
                continue

        # Precio
        if precio_min is not None or precio_max is not None:
            precio = a_numero(evento["precio"])
            if precio is None:
                continue
            if precio_min is not None and precio < precio_min:
                continue
            if precio_max is not None and precio > precio_max:
                continue

        resultados.append(evento)

    return {"total": len(resultados), "eventos": resultados}