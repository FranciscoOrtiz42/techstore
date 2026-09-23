from django.contrib import admin

from .models import Producto, Tienda

# Estos modelos quedan disponibles para gestionar el inventario desde /admin/.
admin.site.register(Tienda)  # Lo registras en el panel de administración
admin.site.register(Producto)

