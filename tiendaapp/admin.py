from django.contrib import admin

# Register your models here.
#superuser: admin pass: 123456


from .models import Tienda  # Importas tu modelo Tienda

admin.site.register(Tienda)  # Lo registras en el panel de administración