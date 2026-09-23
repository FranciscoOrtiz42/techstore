import unicodedata
from difflib import SequenceMatcher

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


def _normalizar_busqueda(texto):
      texto = unicodedata.normalize('NFKD', texto.casefold())
      return ''.join(caracter for caracter in texto if not unicodedata.combining(caracter))


def _coincide_producto(producto, consulta):
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
      todos_productos = Producto.objects.all()
      busqueda = request.GET.get('q', '').strip()
      stock_disponible = todos_productos.aggregate(total=Sum('stock'))['total'] or 0
      stock_bajo = todos_productos.filter(stock__lte=5).count()
      productos = todos_productos
      if busqueda:
            productos = [producto for producto in productos if _coincide_producto(producto, busqueda)]
      return render(request, 'inicio.html', {
            'productos': productos,
            'formulario': ProductoForm(),
            'stock_disponible': stock_disponible,
            'stock_bajo': stock_bajo,
            'busqueda': busqueda,
      })


def lista_productos(request):
      productos = Producto.objects.all()
      return render(request, 'productos.html', {'productos': productos})


def crear_producto(request):
      if request.method != 'POST':
            return redirect('inicio')

      formulario = ProductoForm(request.POST)
      if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto creado correctamente.')
      else:
            messages.error(request, 'No se pudo crear el producto. Revisa los datos.')
      return redirect('inicio')


def editar_producto(request, producto_id):
      producto = get_object_or_404(Producto, pk=producto_id)
      if request.method == 'GET':
            return render(request, 'editar_producto.html', {
                  'producto': producto,
                  'formulario': ProductoForm(instance=producto),
            })

      formulario = ProductoForm(request.POST, instance=producto)
      if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Producto actualizado correctamente.')
      else:
            messages.error(request, 'No se pudo actualizar el producto. Revisa los datos.')
      return redirect('inicio')


def eliminar_producto(request, producto_id):
      if request.method == 'POST':
            producto = get_object_or_404(Producto, pk=producto_id)
            producto.delete()
            messages.success(request, 'Producto eliminado correctamente.')
      return redirect('inicio')
