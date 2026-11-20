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

## 4. Qué NO ha hecho la IA

- El planteamento de la problemática y el diseño general de la aplicación. 
- La decisión de agrupar las categorías del CSV.
- La recopilación y preparación del dataset `eventos.csv`.
- Los estilos (`styles.css`) y las imágenes de categoría.
- Las pruebas finales y la decisión de qué cambios aceptar.


## 5. Verificación y responsabilidad

- Todo el código propuesto por la IA se ha revisado, probado en local y adaptado antes de integrarlo.
- Pruebas realizadas: [describe aquí, por ejemplo: seleccionar cada categoría y comprobar que devuelve eventos, probar los filtros combinados, probar con el servidor apagado].
- El equipo es responsable del código final entregado, con independencia de su origen.

## 6. Limitaciones detectadas

- La IA trabajó solo con los archivos compartidos en la conversación (no con `styles.css` ni con el CSV), por lo que algunas decisiones, como qué imagen asignar a cada grupo, requieren ajuste manual.
- El código generado no se ejecutó en el entorno de la IA; la validación se hizo en local.

## 7. Datos y privacidad

No se han compartido con la IA datos personales ni credenciales. Solo se compartió código fuente del proyecto.

---

*Última actualización: 20 de noviembre de 2026*