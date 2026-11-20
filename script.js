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
  cursos_talleres: "img/cursos.png",
  musica: "img/musica.png",
  espectaculos: "img/espectaculos.png",
  deporte: "img/deportes.png",
  infantil: "img/familia.jpg",
  conferencias: "img/tecnologia.jpg",
  exposicion: "img/arte.jpg",
  fiestas: "img/fiesta.jpg",
  literatura: "img/arte.jpg",
  visitas: "img/arte.jpg",
  aire_libre: "img/aire-libre.jpg",
  otros: "img/otros.png",
  default: "img/otros.png"
};

function obtenerImagenActividad(e) {
  return IMAGENES_CATEGORIA[e.grupo] || IMAGENES_CATEGORIA.default;
}