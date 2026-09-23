import unicodedata
from difflib import SequenceMatcher

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


def _normalizar_busqueda(texto):
      # Permite buscar igual aunque se escriban mayúsculas o se omitan tildes.
      texto = unicodedata.normalize('NFKD', texto.casefold())
      return ''.join(caracter for caracter in texto if not unicodedata.combining(caracter))


def _coincide_producto(producto, consulta):
      # La búsqueda revisa nombre, categoría y descripción con coincidencias flexibles.
      consulta = _normalizar_busqueda(consulta)
      campos = [producto.nombre, producto.categoria, producto.descripcion]

      for campo in campos:
            texto = _normalizar_busqueda(campo or '')
            palabras = texto.split()
            if consulta in texto or any(consulta in palabra for palabra in palabras):
                  return True
            if SequenceMatcher(None, consulta, texto).ratio() >= 0.55:
                  return True
            if any(SequenceMatcher(None, consulta, palabra).ratio() >= 0.75 for palabra in palabras):
                  return True
      return False


def inicio(request):
      # Carga los datos necesarios para el panel principal y sus tarjetas de resumen.
      todos_productos = Producto.objects.all()
      busqueda = request.GET.get('q', '').strip()
      stock_disponible = todos_productos.aggregate(total=Sum('stock'))['total'] or 0
      stock_bajo = todos_productos.filter(stock__lte=5).count()
      productos = todos_productos
      if busqueda:
            # Se filtra en Python para conservar también las coincidencias aproximadas.
            productos = [producto for producto in productos if _coincide_producto(producto, busqueda)]
      return render(request, 'inicio.html', {
            'productos': productos,
            'formulario': ProductoForm(),
            'stock_disponible': stock_disponible,
            'stock_bajo': stock_bajo,
            'busqueda': busqueda,
      })


def lista_productos(request):
      # Vista sencilla del inventario completo.
      productos = Producto.objects.all()
      return render(request, 'productos.html', {'productos': productos})


def crear_producto(request):
      # El alta solo acepta envíos POST desde el formulario de la página principal.
      if request.method != 'POST':
            return redirect('inicio')

      formulario = ProductoForm(request.POST)
      if formulario.is_valid():
            # ProductoForm centraliza las validaciones antes de guardar en la base de datos.
            formulario.save()
            messages.success(request, 'Producto creado correctamente.')
      else:
            messages.error(request, 'No se pudo crear el producto. Revisa los datos.')
      return redirect('inicio')


def editar_producto(request, producto_id):
      # Si el producto no existe, Django devuelve automáticamente una respuesta 404.
      producto = get_object_or_404(Producto, pk=producto_id)
      if request.method == 'GET':
            # En GET se muestran los datos actuales para poder modificarlos.
            return render(request, 'editar_producto.html', {
                  'producto': producto,
                  'formulario': ProductoForm(instance=producto),
            })

      formulario = ProductoForm(request.POST, instance=producto)
      if formulario.is_valid():
            # Pasar instance conserva el registro y actualiza sus datos en lugar de crear otro.
            formulario.save()
            messages.success(request, 'Producto actualizado correctamente.')
      else:
            messages.error(request, 'No se pudo actualizar el producto. Revisa los datos.')
      return redirect('inicio')


def eliminar_producto(request, producto_id):
      # La eliminación se limita a POST para evitar borrados accidentales mediante un enlace.
      if request.method == 'POST':
            producto = get_object_or_404(Producto, pk=producto_id)
            producto.delete()
            messages.success(request, 'Producto eliminado correctamente.')
      return redirect('inicio')
