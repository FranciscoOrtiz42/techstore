document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-confirmar-producto]').forEach(function (formulario) {
        formulario.addEventListener('submit', function (evento) {
            // La validación del servidor sigue siendo la autoridad; este resumen solo confirma la intención.
            const datos = new FormData(formulario);
            const accion = formulario.dataset.confirmarProducto === 'editar' ? 'actualizar' : 'crear';
            const resumen = [
                `Nombre: ${datos.get('nombre') || 'Sin nombre'}`,
                `Categoría: ${datos.get('categoria') || 'Sin categoría'}`,
                `Precio: CLP $${datos.get('precio') || '0'}`,
                `Stock: ${datos.get('stock') || '0'} unidades`,
            ].join('\n');

            if (!window.confirm(`Resumen del producto a ${accion}:\n\n${resumen}\n\n¿Deseas confirmar?`)) {
                evento.preventDefault();
            }
        });
    });
});