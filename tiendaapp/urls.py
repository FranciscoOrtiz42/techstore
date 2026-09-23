from django.urls import path
from . import views

# Rutas públicas de la aplicación y acciones principales del inventario.
urlpatterns = [
    # C: muestra el panel y el formulario de alta.
    path('', views.inicio, name='inicio'),  # Panel principal con resumen e inventario.
    # R: consulta todos los productos guardados.
    path('productos/', views.lista_productos, name='lista_productos'),  # Lista completa.
    # C: recibe el POST del formulario y crea una fila nueva.
    path('productos/crear/', views.crear_producto, name='crear_producto'),  # Alta de productos.
    # U: recibe el identificador de la fila que se va a modificar.
    path('productos/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),  # Edición.
    # D: elimina solo mediante POST para evitar borrados desde un enlace accidental.
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),  # Baja.
]