import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import RoleFactory
from .models import Role


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestRolesViewSet:

    def test_list_roles_success(self, api_client):
        """
        Arrange: Crear 3 roles previos en la base de datos usando RoleFactory.
        Act: Realizar una petición GET al endpoint de listado de roles.
        Assert: Retornar 200 OK y verificar que la lista contiene exactamente 3 elementos.
        """
        RoleFactory.create_batch(3)
        url = reverse('roles:roles-list')

        print("\nTest 1: Realizar una petición GET al endpoint de listado de roles")

        response = api_client.get(url)

        print(f"DEBUG: Respuesta: {response.status_code}")
        print(f"DEBUG: Cantidad de roles: {len(response.data)}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_role_success(self, api_client):
        """
        Arrange: Definir un payload con un nombre de rol válido.
        Act: Realizar una petición POST al endpoint de creación.
        Assert: Retornar 201 Created y verificar que el nombre coincida en la BD.
        """
        url = reverse('roles:roles-list')
        payload = {"name": "Editor"}

        print("\nTest 2:  Realizar una petición POST al endpoint de creación de roles")

        response = api_client.post(url, payload)

        print(f"DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_201_CREATED
        assert Role.objects.filter(name="Editor").exists()

    def test_retrieve_role_detail_success(self, api_client):
        """
        Arrange: Crear un rol específico en la base de datos.
        Act: Realizar una petición GET al detalle de ese rol por su ID.
        Assert: Retornar 200 OK y que el 'name' en la respuesta sea el correcto.
        """
        role = RoleFactory(name="Supervisor")
        url = reverse('roles:roles-detail', kwargs={'pk': role.pk})

        print("\nTest 3: Realizar una petición GET al detalle de ese rol por su ID")

        response = api_client.get(url)

        print(f"DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Supervisor"

    def test_update_role_success(self, api_client):
        """
        Arrange: Crear un rol existente.
        Act: Realizar una petición PATCH para cambiar el nombre del rol.
        Assert: Retornar 200 OK y verificar el cambio de nombre en la base de datos.
        """
        role = RoleFactory(name="Old Name")
        url = reverse('roles:roles-detail', kwargs={'pk': role.pk})
        payload = {"name": "New Name"}

        print("\nTest 4: Realizar una petición PATCH para cambiar el nombre del rol.")

        response = api_client.patch(url, payload)

        print(f"DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_200_OK
        role.refresh_from_db()
        assert role.name == "New Name"

    def test_delete_role_success(self, api_client):
        """
        Arrange: Crear un rol que será eliminado.
        Act: Realizar una petición DELETE al endpoint de detalle.
        Assert: Retornar 204 No Content y verificar que el registro ya no existe.
        """
        role = RoleFactory()
        url = reverse('roles:roles-detail', kwargs={'pk': role.pk})

        print("\nTest 5: Eliminar un rol")

        response = api_client.delete(url)

        print(f"DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Role.objects.filter(pk=role.pk).exists()
