import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Comment
from .factories import CommentFactory
from ..products.factories import ProductFactory
from ..users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def product(db):
    return ProductFactory()


@pytest.mark.django_db
class TestCommentViewSet:

    def test_list_comments_success(self, api_client, user):
        """
        Arrange: Crear comentarios previos en la base de datos.
        Act: Realizar petición GET al listado.
        Assert: Retornar 200 y la cantidad correcta de elementos.
        """
        api_client.force_authenticate(user=user)
        CommentFactory.create_batch(3)
        url = reverse('comments:comments-list')

        print("\nTest 1: Realizar petición GET al listado.")
        print(f"DEBUG: Se han creado {Comment.objects.count()} comentarios")

        response = api_client.get(url)

        print(f"DEBUG: Respuesta: {response.status_code}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_comment_authenticated_user(self, api_client, user, product):
        """
        Arrange: Datos válidos de comentario.
        Act: POST al endpoint de creación.
        Assert: El comentario existe en la BD y el status es 201.
        """
        api_client.force_authenticate(user=user)
        url = reverse('comments:comments-list')
        payload = {
            "comment": "Este es un gran producto",
            "product": product.id,
            "user": user.id
        }

        print("\nTest 2: Enviar petición POST para crear un comentario")

        response = api_client.post(url, payload)

        print(f"DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['comment'] == payload['comment']

    def test_create_comment_unauthenticated_fails(self, api_client, product):
        """
        Act: Intentar crear un comentario sin estar logueado.
        Assert: Retornar 403 Forbidden.
        """
        url = reverse('comments:comments-list')
        payload = {
            "comment": "Texto",
            "product": product.id,
            "user": 999
        }

        print("\nTest 3: Intentar crear un comentario sin estar logueado")

        response = api_client.post(url, payload)

        print(f"DEBUG: Respuesta: {response.status_code}")
        assert response.status_code == status.HTTP_403_FORBIDDEN
