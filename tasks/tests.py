from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserLoginTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_login_success(self):
        """
        Prueba que un usuario puede iniciar sesión correctamente y redirigir a la página 'task'.
        """
        response = self.client.post(reverse('singin'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task'))
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'testuser')

    def test_login_failure_invalid_username(self):
        """
        Prueba que un intento de inicio de sesión con un nombre de usuario inválido falla.
        """
        response = self.client.post(reverse('singin'), {
            'username': 'wronguser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Por favor, ingresa un usuario y contraseña válidos.")
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

    def test_redirect_if_already_logged_in(self):
        """
        Prueba que un usuario autenticado se redirige directamente a la página 'task'.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('singin'))
        self.assertRedirects(response, reverse('task'))

    def test_logout(self):
        """
        Prueba que un usuario puede cerrar sesión correctamente.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('singin'))
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)




