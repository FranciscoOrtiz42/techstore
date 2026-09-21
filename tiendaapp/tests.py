from django.test import TestCase
from django.urls import reverse

from .models import Producto


class ProductoCrudTests(TestCase):
	def test_crear_producto(self):
		response = self.client.post(reverse('crear_producto'), {
			'nombre': 'Teclado mecánico',
			'categoria': 'Periféricos',
			'precio': '79.90',
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
			precio='199.99',
			stock=3,
		)

		response = self.client.post(reverse('editar_producto', args=[producto.id]), {
			'nombre': 'Monitor 4K',
			'categoria': 'Monitores',
			'precio': '249.99',
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
