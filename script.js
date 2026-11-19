const btnToggleCategoria = document.getElementById('btn-toggle-categoria');
const menuCategorias = document.getElementById('menu-categorias');
const textoCategoria = document.getElementById('texto-categoria');
const flechaCategoria = document.getElementById('flecha-categoria');
const inputFiltroCategoria = document.getElementById('filtro-categoria');
const botonesCategoria = document.querySelectorAll('.btn-opcion-cat');

// Abrir o cerrar el desplegable de categorías
btnToggleCategoria.addEventListener('click', () => {
  const estaOculto = menuCategorias.classList.toggle('oculto');
  flechaCategoria.textContent = estaOculto ? '▼' : '▲';
});

// Seleccionar una de las 12 categorías
botonesCategoria.forEach((boton) => {
  boton.addEventListener('click', () => {
    botonesCategoria.forEach((b) => b.classList.remove('activo'));
    boton.classList.add('activo');

    textoCategoria.textContent = boton.textContent;
    inputFiltroCategoria.value = boton.dataset.valor;

    // Avisar a script_backend.js de que el filtro ha cambiado para que busque de nuevo
    inputFiltroCategoria.dispatchEvent(new Event('input'));

    menuCategorias.classList.add('oculto');
    flechaCategoria.textContent = '▼';
  });
});

const IMAGENES_CATEGORIA = {
  musica: "img/musica.jpg",
  deporte: "img/deporte.jpg",
  teatro: "img/teatro.jpg",
  arte: "img/arte.jpg",
  gastronomia: "img/gastronomia.jpg",
  cine: "img/cine.jpg",
  tecnologia: "img/tecnologia.jpg",
  "aire-libre": "img/aire-libre.jpg",
  talleres: "img/talleres.jpg",
  fiesta: "img/fiesta.jpg",
  familia: "img/familia.jpg",
  default: "img/default.jpg" // Imagen por defecto si llega una categoría distinta
};

function obtenerImagenActividad(e) {
  const raw = (e.categoria || e.grupo_id || e.grupo_nombre || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, "-");

  return IMAGENES_CATEGORIA[raw] || IMAGENES_CATEGORIA.default;
}
