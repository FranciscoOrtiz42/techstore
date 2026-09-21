from django.contrib import admin

from .models import Producto, Tienda

admin.site.register(Tienda)  # Lo registras en el panel de administración
admin.site.register(Producto)

