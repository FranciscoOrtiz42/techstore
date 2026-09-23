from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Modelo que conserva la estructura inicial del proyecto.
class Tienda(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    completada = models.BooleanField(default=False)


# Producto que aparece en el inventario de la tienda.
class Producto(models.Model):
    # Entidad principal del CRUD: cada fila representa un producto persistido en la base de datos.
    nombre = models.CharField(max_length=150)  # Nombre que se muestra en el catálogo.
    categoria = models.CharField(max_length=100)  # Tipo de producto al que pertenece.
    descripcion = models.TextField(blank=True)  # Puede quedar vacía al registrar un producto.
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        # CLP se maneja sin decimales y el negocio exige un mínimo de $1.000.
        validators=[MinValueValidator(1000)],
    )  # Precio expresado en pesos CLP enteros.
    stock = models.PositiveIntegerField(
        default=0,
        # PositiveIntegerField evita negativos; este validador fija además el máximo del negocio.
        validators=[MaxValueValidator(9999)],
    )  # Unidades disponibles, entre 0 y 9999.
    creado_en = models.DateTimeField(auto_now_add=True)  # Se asigna solo al crear el registro.
    actualizado_en = models.DateTimeField(auto_now=True)  # Se actualiza cada vez que cambia.

    class Meta:
        # Los productos más recientes aparecen primero en el inventario.
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre

