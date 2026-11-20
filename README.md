# 🐱 MiauVentos: explora eventos en Madrid

Aplicación web para descubrir actividades culturales y de ocio en Madrid a partir de los **datos abiertos del Ayuntamiento de Madrid**. Muestra los próximos eventos ordenados por fecha y permite filtrarlos por categoría (una o varias), fecha, hora de inicio, precio, duración y distancia a tu ubicación.

Proyecto desarrollado para la hackatón **2Campus1Code (DAETSISI · DAETSIINF · ORANGE)**.

## 🏗️ Cómo está hecho

| Parte | Archivos | Qué hace |
|---|---|---|
| Backend | `main.py` | API con **FastAPI** que lee `data/eventos.csv` y filtra los eventos |
| Frontend | `index.html`, `styles.css`, `script.js`, `script_backend.js`, `img/` | Web en HTML, CSS y JavaScript sin frameworks. Llama a la API en `http://127.0.0.1:8000` |
| Datos | `data/` | CSV con los eventos ya limpios y unidos, y `ESQUEMA.md` con el detalle de cada campo |

Endpoints de la API:

- `GET /api/categorias`: categorías y número de eventos de cada una.
- `GET /api/eventos`: eventos filtrados. Admite `categoria` (varias separadas por coma), `fecha_desde`, `fecha_hasta`, `inicio_desde`, `inicio_hasta`, `precio_min`, `precio_max`, `duracion_min` y `duracion_max`.

## ▶️ Cómo ejecutarlo

### Requisitos

- **Python 3.9 o superior** (probado con Python 3.13).
- Un navegador web moderno (Chrome, Firefox, Edge...).

### 1. Descargar el proyecto

```bash
git clone https://github.com/Xposito/CivicPulseAI.git
cd CivicPulseAI
```

### 2. Instalar las dependencias

Recomendamos usar un entorno virtual:

```bash
python -m venv venv
```

Actívalo:

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

E instala FastAPI y Uvicorn:

```bash
pip install fastapi uvicorn
```

> En macOS o Linux puede que tengas que usar `python3` en lugar de `python`.

### 3. Arrancar el backend

Desde la carpeta del proyecto (donde está `main.py`):

```bash
uvicorn main:app --reload
```

Cuando veas `Uvicorn running on http://127.0.0.1:8000`, la API ya está funcionando. Puedes comprobarlo abriendo:

- <http://127.0.0.1:8000/api/categorias> (debe devolver una lista en JSON)
- <http://127.0.0.1:8000/docs> (documentación interactiva de la API)

Deja esta terminal abierta mientras uses la web.

### 4. Abrir el frontend

Con el backend encendido, abre `index.html` en el navegador (doble clic en el archivo). No hace falta ningún servidor extra: la API permite peticiones desde cualquier origen.

Si prefieres servirlo, también funciona con la extensión **Live Server** de VS Code o con:

```bash
python -m http.server 5500
```

y entrando en <http://localhost:5500>.

### ❓ Problemas frecuentes

- **La web dice "No se pudo conectar con el servidor. ¿Está encendido?"**: el backend no está arrancado o no está en el puerto 8000. Repite el paso 3.
- **`uvicorn` no se reconoce como comando**: activa el entorno virtual o usa `python -m uvicorn main:app --reload`.
- **El puerto 8000 está ocupado**: cierra el otro programa que lo usa. Si arrancas en otro puerto, cambia también la constante `API` al principio de `script_backend.js`.
- **No salen eventos**: la API solo muestra eventos desde hoy en adelante. Los datos son una descarga fija, así que con el tiempo habrá menos eventos futuros.

## 📊 Fuentes de datos

Todos los datos proceden del **[Portal de Datos Abiertos del Ayuntamiento de Madrid](https://datos.madrid.es)** y se usan bajo licencia **CC BY 4.0**. Datos: Ayuntamiento de Madrid.

**Eventos** (forman `data/eventos.csv`, que usa el backend):

1. [Agenda de actividades y eventos](https://datos.madrid.es/dataset/300107-0-agenda-actividades-eventos)
2. [Actividades culturales y de ocio municipal en los próximos 100 días](https://datos.madrid.es/dataset/206974-0-agenda-eventos-culturales-100)
3. [Actividades gratuitas en Bibliotecas Municipales en los próximos 60 días](https://datos.madrid.es/dataset/206717-0-agenda-eventos-bibliotecas)
4. [Agenda de actividades deportivas](https://datos.madrid.es/dataset/212504-0-agenda-actividades-deportes)

**Lugares** (se cruzan con los eventos para completar dirección, coordenadas y distrito):

5. [Museos de la ciudad de Madrid](https://datos.madrid.es/dataset/201132-0-museos)
6. [Bibliotecas de Madrid](https://datos.madrid.es/dataset/201747-0-bibliobuses-bibliotecas)
7. [Centros culturales municipales](https://datos.madrid.es/dataset/200304-0-centros-culturales)
8. [Centros deportivos municipales (polideportivos)](https://datos.madrid.es/dataset/200186-0-polideportivos)

**Otros CSV originales** (en `data/originales/`, unidos en `data/actividades_unidas.csv`):

- [Cursos y talleres en los centros culturales de los distritos](https://datos.madrid.es/dataset/50064-0-talleres-culturales-cursos)
- [Conciertos y plantilla de la Banda Sinfónica Municipal de Madrid](https://datos.madrid.es/dataset/135161-0-conciertos-y-personal-de-la-banda-sinfonica-municipal-de-madrid)

Cómo se limpiaron, unieron y categorizaron los datos: [`data/ESQUEMA.md`](data/ESQUEMA.md).

## 🤖 Uso de IA

Las herramientas de IA utilizadas y su contribución están descritas en [`AI_USAGE.md`](AI_USAGE.md).

## 📄 Licencia

Código bajo licencia MIT (ver [`LICENSE`](LICENSE)). Los datos pertenecen al Ayuntamiento de Madrid (CC BY 4.0).
