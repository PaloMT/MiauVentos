# Uso de inteligencia artificial en el proyecto

Este documento recoge de forma transparente cómo se ha utilizado IA durante el desarrollo de **MiauVentos** (explorador de eventos de Madrid).

## 1. Herramientas utilizadas

| Herramienta | Proveedor | Para qué se usó |
|---|---|---|
| Claude | Anthropic | Revisión de código, detección de errores de integración entre frontend y backend y generación de fragmentos de código |
| Gemini | Google | Diseño del prototipo, depuración de código, creación del filtrado dinámico |

## 2. Resumen del proyecto

- **Backend:** API en Python con FastAPI (`main.py`) que carga los eventos desde `data/eventos.csv` y los expone en `/api/categorias` y `/api/eventos`.
- **Frontend:** HTML, CSS y JavaScript sin frameworks (`index.html`, `script.js`, `script_backend.js`), con filtros por categoría, hora, precio, distancia y duración.

## 3. Dónde se ha usado la IA

### 3.1 Corrección del sistema de categorías

**Problema:** el HTML tenía 11 categorías escritas a mano (`teatro`, `arte`, `gastronomia`...) que no coincidían con los `id` de los grupos definidos en `main.py` (`espectaculos`, `cursos_talleres`, `fiestas`...). Solo coincidían `musica` y `deporte`, así que el resto de filtros devolvía 0 resultados. Además, `script_backend.js` trataba un `<input type="hidden">` como si fuera un `<select>` y nunca llamaba a `cargarCategorias()`.

**Qué propuso la IA:**
- Eliminar las categorías fijas del HTML y pintarlas dinámicamente desde `/api/categorias`.
- Usar delegación de eventos en `script.js` para que funcionen los botones creados dinámicamente.
- Reescribir `cargarCategorias()` en `script_backend.js` para crear los botones y llamarla en el arranque.
- Asociar las imágenes de las tarjetas al campo `grupo` en lugar de a la categoría del CSV.

**Archivos afectados:** `index.html`, `script.js`, `script_backend.js`.

### 3.2 Generación de `script_backend.js`

La IA generó la versión completa del archivo con los cambios anteriores integrados. El resto de la lógica (filtros, cálculo de distancia, paginación, pintado de tarjetas) ya existía y se mantuvo.

### 3.3 Este documento

La estructura y el borrador de `IA_USAGE.md` también se generaron con IA y después se revisaron por el equipo.

### 3.4 Interfaz de usuario

Tras revisar un primer prototipo completo, se optó por un enfoque práctico sin librerías externas. Se estructuró la interfaz en HTML y CSS puro, se creó el menú desplegable y el filtrado dinámico en JavaScript, y se añadieron dinámicamente las . Luego se resolvieron errores de sintaxis y conflictos de variables entre los scripts y la lógica de conexión con la API (script_backend.js).

### 3.5 Descarga y normalización de los datos abiertos (Claude)

- Claude escribió un script en Python, sin librerías externas, que descarga 8 datasets de actividades culturales del Portal de Datos Abiertos del Ayuntamiento de Madrid (<https://datos.madrid.es>, licencia CC BY 4.0).
- El script unifica los campos, elimina duplicados, clasifica las actividades por categorías y cruza cada evento con su lugar (dirección, distrito, coordenadas).
- Documentó fuentes, esquema y decisiones en [`data/ESQUEMA.md`](data/ESQUEMA.md), y generó versiones en CSV plano separando eventos y lugares.
- Muchas actividades quedaban en «Otros». Claude propuso cómo reclasificarlas y el equipo revisó las propuestas por tandas antes de aplicarlas.

### 3.6 Unión de los CSV originales (Claude)

- A petición del equipo, hizo un *outer join* de los 4 CSV originales (`data/originales/`) en [`data/actividades_unidas.csv`](data/actividades_unidas.csv). Antes de unirlos enseñó cómo pensaba emparejar las columnas y esperó a que lo confirmáramos.
- Añadió la columna `CATEGORIA`, que asigna cada actividad a una de 15 categorías fijas.
- Adaptó `data/eventos.csv` al formato que ya leía `main.py`, con un script auxiliar, para usar los datos nuevos sin tocar el backend en ese momento.

### 3.7 Filtros por fecha y formato europeo (Claude)

- **Filtro por fecha:** en `main.py` añadió `fecha_desde` (por defecto, hoy) y `fecha_hasta`, teniendo en cuenta `dias_semana` y `dias_excluidos`. Los resultados se ordenan por la próxima sesión y la API devuelve `proxima_fecha`, que la tarjeta muestra. Se añadieron los campos de fecha en `index.html` y `styles.css`, y su envío en `script_backend.js`.
- **Formato dd/mm/aaaa y 24 h:** los campos de fecha y hora se rellenan solos con formato europeo y el botón abre el selector del navegador, pero el valor siempre se escribe como `dd/mm/aaaa` o `hh:mm`.
- El filtro de una o varias categorías (apartado 3.1) se completó con las 15 categorías finales en `main.py`.

### 3.8 Pruebas de la aplicación (Claude)

- Probó la web de principio a fin con un navegador automatizado: filtros sueltos y combinados, búsquedas sin resultados, vista de escritorio y servidor apagado, con capturas de cada caso.
- Encontró varios fallos: el HTML cargaba un `scripts.js` que no existía, se aceptaban horas inválidas y el orden de los resultados no era el esperado.
- Propuso los arreglos como un *diff* sin aplicarlos; el equipo decidió cuáles incorporar.

### 3.9 Git y estado del repositorio (Claude)

- Resúmenes del estado del repositorio (qué había cambiado y en qué estaba cada uno).
- Ayuda para resolver un conflicto de fusión, respetando los ficheros que el equipo había borrado a propósito.
- Claude no hacía commits ni push sin permiso explícito del equipo. Los commits que lleva su firma (`Co-Authored-By: Claude`) se hicieron con esa autorización.

## 4. Qué NO ha hecho la IA

- El planteamento de la problemática y el diseño general de la aplicación. 
- La decisión de agrupar las categorías del CSV.
- La elección de las fuentes de datos y la validación final de `eventos.csv`. La IA ayudó a descargarlo y prepararlo (apartados 3.5 y 3.6), pero las decisiones sobre su contenido fueron del equipo.
- Los estilos (`styles.css`) y las imágenes de categoría.
- Las pruebas finales y la decisión de qué cambios aceptar.
- Las decisiones de producto, como descartar el mapa que se planteó al principio o rehacer el CSV a nuestra manera en lugar de quedarnos con la primera versión generada.


## 5. Verificación y responsabilidad

- Todo el código propuesto por la IA se ha revisado, probado en local y adaptado antes de integrarlo.
- Pruebas realizadas: seleccionar cada categoría y comprobar que devuelve eventos, combinar filtros (categoría, fecha, hora, precio, distancia y duración), búsquedas sin resultados, vista de escritorio y comportamiento con el servidor apagado (ver apartado 3.8).
- El equipo es responsable del código final entregado, con independencia de su origen.

## 6. Limitaciones detectadas

- La IA trabajó solo con los archivos compartidos en la conversación (no con `styles.css` ni con el CSV), por lo que algunas decisiones, como qué imagen asignar a cada grupo, requieren ajuste manual.
- El código generado no se ejecutó en el entorno de la IA; la validación se hizo en local.

## 7. Datos y privacidad

No se han compartido con la IA datos personales ni credenciales. Solo se compartió código fuente del proyecto.

---

*Última actualización: 20 de noviembre de 2026*