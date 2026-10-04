from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .forms import ProductoForm
from .models import Producto


class ProductoCrudTests(TestCase):
	def setUp(self):
		usuario = get_user_model().objects.create_superuser(
			username='usuario_prueba',
			password='clave-prueba-123',
		)
		self.client.force_login(usuario)

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


class LoginTests(TestCase):
	def setUp(self):
		self.usuario = get_user_model().objects.create_superuser(
			username='usuario_prueba',
			password='clave-prueba-123',
		)

	def test_login_valido(self):
		response = self.client.post(reverse('login'), {
			'username': 'usuario_prueba',
			'password': 'clave-prueba-123',
		})

		self.assertRedirects(response, reverse('inicio'))

	def test_login_rechaza_credenciales_incorrectas(self):
		response = self.client.post(reverse('login'), {
			'username': 'usuario_prueba',
			'password': 'incorrecta',
		})

		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.wsgi_request.user.is_authenticated)

	def test_inicio_requiere_login(self):
		response = self.client.get(reverse('inicio'))

		self.assertRedirects(
			response,
			f"{reverse('login')}?next={reverse('inicio')}",
		)
