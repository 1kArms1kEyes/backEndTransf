import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from .factories import UserFactory

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestUserAuth:

    def test_register_user_success(self, api_client):
        """
        Arrange: Definir datos válidos para un nuevo usuario.
        Act: Realizar petición POST al endpoint de registro.
        Assert: Retornar 201 Created y verificar que el usuario existe en la BD.
        """
        url = reverse('users:register')
        payload = {
            "username": "new_user",
            "password": "password123",
            "email": "new@test.com",
        }

        print("\nTest 1: Realizar petición POST al endpoint de registro de usuario")
        response = api_client.post(url, payload)

        print(f"DEBUG: Respuesta: {response.status_code}")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="new_user").exists()

    def test_login_success_returns_token(self, api_client):
        """
        Arrange: Crear un usuario con credenciales conocidas en la BD.
        Act: Realizar petición POST al endpoint de login con dichas credenciales.
        Assert: Retornar 200 OK y verificar que se devuelve un token válido.
        """

        password = "secret_password"
        user = UserFactory(password=password)
        url = reverse('users:login')

        payload = {
            "username": user.username,
            "password": password
        }

        print("\nTest 2: Realizar petición POST al endpoint de login con credenciales correctas")

        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

        print(f"DEBUG: Respuesta: {response.status_code}")
        token_exists = Token.objects.filter(key=response.data['token'], user=user).exists()
        assert token_exists

    def test_login_invalid_credentials(self, api_client):
        """
        Arrange: Crear un usuario en la BD.
        Act: Intentar login con una contraseña incorrecta.
        Assert: Retornar 401 Unauthorized y un mensaje de error.
        """
        user = UserFactory(password="correct_password")
        url = reverse('users:login')
        payload = {
            "username": user.username,
            "password": "wrong_password"
        }

        print("\nTest 3: Intentar login con una contraseña incorrecta.")

        response = api_client.post(url, payload)

        print(f"DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data


@pytest.mark.django_db
class TestUsersViewSet:

    def test_list_users_success(self, api_client):
        """
        Arrange: Crear múltiples usuarios usando UserFactory.
        Act: Realizar petición GET al listado general de usuarios.
        Assert: Retornar 200 OK y la lista con la cantidad esperada de registros.
        """
        UserFactory.create_batch(5)
        url = reverse('users:users-list')

        print("\nTest 4: Realizar petición GET al listado general de usuarios")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        print(f"DEBUG: Respuesta: {response.status_code}")
        print(f"Listado de usuarios: {response.data}")
        print(f"DEBUG: Cantidad de usuario creados {len(response.data)}")
        assert len(response.data) >= 5
