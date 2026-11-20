#!/usr/bin/env python3
"""
Convierte data/actividades_unidas.csv al formato que lee main.py
(data/eventos.csv, separado por comas, UTF-8) sin tener que tocar main.py.

    python3 data/preparar_backend.py

- Primero van las 23 columnas que main.py lee por nombre (id, titulo, categoria,
  gratis, precio_min, fecha_inicio, hora_inicio, duracion_min, lat, lon...).
- Detrás van TODAS las columnas originales de actividades_unidas.csv, con su
  nombre de siempre. main.py no las usa, pero están en cada fila.
- No se inventa nada: si un dato no está en el CSV original, se deja vacío.
"""

import csv
import re
from datetime import date, datetime, timedelta
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
ENTRADA = CARPETA / "actividades_unidas.csv"
SALIDA = CARPETA / "eventos.csv"

# Columnas que main.py lee con fila["..."] (en este orden)
COLUMNAS_BACKEND = [
    "id", "titulo", "categoria", "categoria_nombre", "subcategoria",
    "gratis", "precio_min", "precio_texto",
    "fecha_inicio", "fecha_fin", "hora_inicio", "hora_fin", "duracion_min",
    "estado", "publico", "lugar_nombre", "direccion", "distrito", "barrio",
    "lat", "lon", "descripcion", "url",
]

# CATEGORIA (nombre de las 15) -> id que espera GRUPOS en main.py
ID_CATEGORIA = {
    "Cursos y talleres": "taller", "Música": "musica", "Teatro y circo": "teatro", "Cine": "cine",
    "Deporte": "deporte", "Infantil": "infantil", "Conferencias": "conferencia",
    "Exposición": "exposicion", "Fiestas y festivales": "fiestas", "Danza": "danza",
    "Literatura y recitales": "literatura", "Visitas e itinerarios": "visita_guiada",
    "Aire libre y medio ambiente": "aire_libre", "Club de lectura": "club_lectura", "Otros": "otros",
}

DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]


def minutos(texto):
    """'1 hora, 30 min' -> 90 ; 'Duración: 60 minutos' -> 60 ; sin dato -> ''"""
    t = (texto or "").lower()
    h = re.search(r"(\d+)\s*hora", t)
    m = re.search(r"(\d+)\s*min", t)
    if not h and not m:
        return ""
    return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)


def duracion_en_descripcion(texto):
    m = re.search(r"duraci[oó]n[^0-9]{0,30}(\d+\s*(?:minutos|min|horas?)(?:\s*y\s*media)?)", texto or "", re.I)
    if not m:
        return ""
    n = minutos(m.group(1))
    if n != "" and "media" in m.group(1).lower():
        n += 30
    return n


def precio_minimo(texto):
    numeros = [float(n.replace(",", ".")) for n in re.findall(r"(\d+(?:[.,]\d+)?)\s*(?:€|euro)", texto or "", re.I)]
    if not numeros:
        return ""
    p = min(numeros)
    return int(p) if p == int(p) else p


def sumar(hora, mins):
    if not hora or mins == "":
        return ""
    try:
        return (datetime.strptime(hora, "%H:%M") + timedelta(minutes=mins)).strftime("%H:%M")
    except ValueError:
        return ""


def convertir(f, n, hoy):
    fuente = f["FUENTE"]
    fecha_ini, fecha_fin = f["FECHA"][:10], f["FECHA-FIN"][:10]
    hora = f["HORA"]
    dur = ""

    if fuente == "Talleres":
        # Hora y duración del primer día de la semana que tenga hora
        for d in DIAS:
            if f[f"HORA_INICIO_{d}"].strip():
                hora = f[f"HORA_INICIO_{d}"].strip()
                dur = minutos(f[f"DURACION_ACTIVIDAD_{d}"])
                break
    else:
        dur = duracion_en_descripcion(f["DESCRIPCION"])

    if fuente == "Talleres":
        estado = "en_curso"
    elif fecha_fin and fecha_fin < hoy:
        estado = "pasado"
    elif fecha_ini and fecha_ini > hoy:
        estado = "proximo"
    elif fecha_ini and not fecha_fin and fecha_ini < hoy:
        estado = "pasado"   # conciertos de la Banda (solo tienen una fecha)
    else:
        estado = "en_curso"

    if f["GRATUITO"] == "1":
        gratis = "true"
    elif f["GRATUITO"] == "0":
        gratis = "false"
    else:
        gratis = ""

    direccion = " ".join(x for x in (f["CLASE-VIAL-INSTALACION"], f["NOMBRE-VIA-INSTALACION"],
                                     f["NUM-INSTALACION"]) if x.strip())
    if f["ID-EVENTO"].strip():
        ident = f"evento-{f['ID-EVENTO'].strip()}"
    else:
        ident = f"{fuente.lower()}-{n}"

    return {
        "id": ident,
        "titulo": f["TITULO"],
        "categoria": ID_CATEGORIA.get(f["CATEGORIA"], "otros"),
        "categoria_nombre": f["CATEGORIA"],
        "subcategoria": f["TIPO"].rstrip("/").split("/")[-1] if f["TIPO"] else "",
        "gratis": gratis,
        "precio_min": 0 if gratis == "true" else precio_minimo(f["PRECIO"]),
        "precio_texto": f["PRECIO"],
        "fecha_inicio": fecha_ini,
        "fecha_fin": fecha_fin,
        "hora_inicio": hora,
        "hora_fin": sumar(hora, dur),
        "duracion_min": dur,
        "estado": estado,
        "publico": ";".join(p.split("/")[-1] for p in f["PUBLICO"].split(",") if p.strip()),
        "lugar_nombre": f["LUGAR"],
        "direccion": direccion,
        "distrito": f["DISTRITO"],
        "barrio": f["BARRIO-INSTALACION"],
        "lat": f["LATITUD"],
        "lon": f["LONGITUD"],
        "descripcion": f["DESCRIPCION"],
        "url": f["CONTENT-URL"],
    }


def main():
    hoy = date.today().isoformat()
    with open(ENTRADA, encoding="utf-8-sig", newline="") as fh:
        lector = csv.DictReader(fh, delimiter=";")
        originales = lector.fieldnames
        filas = list(lector)

    columnas = COLUMNAS_BACKEND + [c for c in originales if c not in COLUMNAS_BACKEND]
    contador = {}
    with open(SALIDA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, delimiter=",")
        w.writeheader()
        for f in filas:
            contador[f["FUENTE"]] = contador.get(f["FUENTE"], 0) + 1
            w.writerow({**f, **convertir(f, contador[f["FUENTE"]], hoy)})
    print(f"{SALIDA.name}: {len(filas)} filas, {len(columnas)} columnas")


if __name__ == "__main__":
    main()
