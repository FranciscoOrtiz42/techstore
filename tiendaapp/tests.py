from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from .forms import ProductoForm
from .models import Producto


class ProductoCrudTests(TestCase):
	def test_validaciones_de_precio_clp(self):
		base_data = {
			'nombre': 'Teclado mecánico',
			'categoria': 'Periféricos',
			'stock': '10',
			'descripcion': 'Teclado RGB',
		}

		for precio in ('999.90', '999', '10000000000'):
			form = ProductoForm({**base_data, 'precio': precio})
			self.assertFalse(form.is_valid(), precio)

		stock_form = ProductoForm({**base_data, 'precio': '1000', 'stock': '10000'})
		self.assertFalse(stock_form.is_valid())

		producto = Producto(
			nombre='Monitor',
			categoria='Monitores',
			precio='999.50',
			stock=3,
		)
		with self.assertRaises(ValidationError):
			producto.full_clean()

		producto.stock = 10000
		with self.assertRaises(ValidationError):
			producto.full_clean()

	def test_crear_producto(self):
		response = self.client.post(reverse('crear_producto'), {
			'nombre': 'Teclado mecánico',
			'categoria': 'Periféricos',
			'precio': '1000',
			'stock': '10',
			'descripcion': 'Teclado RGB',
		})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('inicio'))
		self.assertTrue(Producto.objects.filter(nombre='Teclado mecánico').exists())

	def test_editar_y_eliminar_producto(self):
		producto = Producto.objects.create(
			nombre='Monitor',
			categoria='Monitores',
			precio='1990',
			stock=3,
		)

		response = self.client.post(reverse('editar_producto', args=[producto.id]), {
			'nombre': 'Monitor 4K',
			'categoria': 'Monitores',
			'precio': '2490',
			'stock': '5',
			'descripcion': 'Panel IPS',
		})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('inicio'))
		producto.refresh_from_db()
		self.assertEqual(producto.nombre, 'Monitor 4K')

		response = self.client.post(reverse('eliminar_producto', args=[producto.id]))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('inicio'))
		self.assertFalse(Producto.objects.filter(id=producto.id).exists())
