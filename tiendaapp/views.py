from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


def inicio(request):
      productos = Producto.objects.all()
      return render(request, 'inicio.html', {
            'productos': productos,
            'formulario': ProductoForm(),
      })


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
