import csv
import unicodedata
from datetime import datetime, time
from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de eventos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambia "*" por tu dominio
    allow_methods=["*"],
    allow_headers=["*"],
)

# main.py junto a la carpeta data/. Si main.py está dentro de data/, quita "data".
RUTA_CSV = Path(__file__).parent / "data" / "eventos.csv"


# ---------- Utilidades ----------

def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes: 'Música' -> 'musica'."""
    texto = unicodedata.normalize("NFD", texto or "")
    return "".join(c for c in texto if unicodedata.category(c) != "Mn").lower().strip()


def a_numero(valor: str) -> Optional[float]:
    try:
        return float(valor.strip().replace(",", "."))
    except (ValueError, AttributeError):
        return None


def a_hora(valor: str) -> Optional[time]:
    try:
        return datetime.strptime(valor.strip(), "%H:%M").time()
    except (ValueError, AttributeError):
        return None


# ---------- Carga del CSV (una sola vez) ----------

@lru_cache(maxsize=1)
def cargar_eventos() -> list[dict]:
    eventos = []
    # utf-8-sig por si el CSV trae BOM (típico al guardar desde Excel)
    with open(RUTA_CSV, mode="r", encoding="utf-8-sig", newline="") as f:
        for fila in csv.DictReader(f, delimiter=","):
            gratis = fila["gratis"].strip().lower() == "true"
            precio = 0.0 if gratis else a_numero(fila["precio_min"])  # None = precio desconocido

            eventos.append({
                # Datos para mostrar en el HTML
                "id": fila["id"],
                "titulo": fila["titulo"],
                "categoria": fila["categoria"],
                "categoria_nombre": fila["categoria_nombre"],
                "subcategoria": fila["subcategoria"],
                "gratis": gratis,
                "precio": precio,
                "precio_texto": fila["precio_texto"],
                "fecha_inicio": fila["fecha_inicio"],
                "fecha_fin": fila["fecha_fin"],
                "hora_inicio": fila["hora_inicio"],
                "hora_fin": fila["hora_fin"],
                "duracion_min": int(a_numero(fila["duracion_min"]) or 0),
                "estado": fila["estado"],
                "publico": fila["publico"],
                "lugar_nombre": fila["lugar_nombre"],
                "direccion": fila["direccion"],
                "distrito": fila["distrito"],
                "barrio": fila["barrio"],
                "lat": a_numero(fila["lat"]),
                "lon": a_numero(fila["lon"]),
                "descripcion": fila["descripcion"],
                "url": fila["url"],
                # Campos internos para filtrar (se quitan antes de responder)
                "_hora": a_hora(fila["hora_inicio"]),
                "_cat": normalizar(fila["categoria"]) + " " + normalizar(fila["categoria_nombre"]),
            })
    return eventos


def publico(evento: dict) -> dict:
    return {k: v for k, v in evento.items() if not k.startswith("_")}


# ---------- Endpoints ----------

@app.get("/api/categorias")
def obtener_categorias():
    """Lista de categorías para rellenar un <select> en el HTML."""
    vistas = {}
    for e in cargar_eventos():
        vistas[e["categoria"]] = e["categoria_nombre"]
    return [{"valor": k, "nombre": v} for k, v in sorted(vistas.items(), key=lambda kv: kv[1])]


@app.get("/api/eventos")
def obtener_eventos(
    categoria: Optional[str] = Query(None, description="Ej: musica, teatro, taller"),
    duracion_min: Optional[int] = Query(None, ge=0, description="Minutos"),
    duracion_max: Optional[int] = Query(None, ge=0, description="Minutos"),
    inicio_desde: Optional[str] = Query(None, pattern=r"^\d{2}:\d{2}$", description="HH:MM"),
    inicio_hasta: Optional[str] = Query(None, pattern=r"^\d{2}:\d{2}$", description="HH:MM"),
    precio_min: Optional[float] = Query(None, ge=0),
    precio_max: Optional[float] = Query(None, ge=0),
):
    cat = normalizar(categoria) if categoria else None
    desde = a_hora(inicio_desde) if inicio_desde else None
    hasta = a_hora(inicio_hasta) if inicio_hasta else None

    resultados = []

    for e in cargar_eventos():
        # Categoría (parcial, sin mayúsculas ni tildes)
        if cat and cat not in e["_cat"]:
            continue

        # Duración
        if duracion_min is not None and e["duracion_min"] < duracion_min:
            continue
        if duracion_max is not None and e["duracion_min"] > duracion_max:
            continue

        # Hora de inicio (los eventos sin hora quedan fuera si filtras por hora)
        if desde or hasta:
            if e["_hora"] is None:
                continue
            if desde and e["_hora"] < desde:
                continue
            if hasta and e["_hora"] > hasta:
                continue

        # Precio (los eventos con precio desconocido quedan fuera si filtras por precio)
        if precio_min is not None or precio_max is not None:
            if e["precio"] is None:
                continue
            if precio_min is not None and e["precio"] < precio_min:
                continue
            if precio_max is not None and e["precio"] > precio_max:
                continue

        resultados.append(publico(e))

    return {"total": len(resultados), "eventos": resultados}