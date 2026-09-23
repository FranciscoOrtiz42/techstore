from django.urls import path
from . import views

# Rutas públicas de la aplicación y acciones principales del inventario.
urlpatterns = [
    path('', views.inicio, name='inicio'),  # Panel principal con resumen e inventario.
    path('productos/', views.lista_productos, name='lista_productos'),  # Lista completa.
    path('productos/crear/', views.crear_producto, name='crear_producto'),  # Alta de productos.
    path('productos/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),  # Edición.
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),  # Baja.
]