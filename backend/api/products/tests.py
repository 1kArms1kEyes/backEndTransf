import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .factories import (
    ProductFactory,
    BrandFactory,
    ColorFactory,
    NetworkFactory,
    OSFactory
)
from .models import Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestProductViewSet:

    def test_list_products_with_filters_success(self, api_client):
        """
        Arrange: Crear un producto específico y varios genéricos.
        Act: Realizar petición GET filtrando por el nombre del producto específico.
        Assert: Retornar 200 OK y que el resultado contenga solo el producto filtrado.
        """
        target_name = "SuperPhone X"
        ProductFactory(name=target_name)
        ProductFactory.create_batch(2, name="Other Phone")

        print("\nTest 1: Realizar petición GET filtrando por el nombre del producto específico")

        url = reverse('products:products-list')
        response = api_client.get(url, {'search': target_name})

        print(f"DEBUG: Respuesta: {response.status_code}")
        print(f"DEBUG: Lista de productos: {response.data}")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == target_name

    def test_create_product_success(self, api_client):
        """
        Arrange: Crear las dependencias (Brand, Color, etc.) y definir el payload.
        Act: Realizar petición POST para crear un nuevo producto.
        Assert: Retornar 201 Created y verificar que los datos técnicos se guardaron bien.
        """
        brand = BrandFactory()
        color = ColorFactory()
        network = NetworkFactory()
        os = OSFactory()

        url = reverse('products:products-list')
        payload = {
            "name": "Test Mobile",
            "storage": 256,
            "ram": 12,
            "release_date": "2024-01-01",
            "max_battery": 5000,
            "main_camera_res": 108.0,
            "selfie_camera_res": 32.0,
            "synopsis": "A great test phone",
            "brand": brand.id,
            "color": color.id,
            "max_supported_network": network.id,
            "operating_system": os.id
        }

        print("\nTest 2: Crear un nuevo producto")

        response = api_client.post(url, payload)

        print("DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.get(name="Test Mobile").ram == 12


@pytest.mark.django_db
class TestProductFilterOptions:

    def test_get_filter_options_success(self, api_client):
        """
        Arrange: Crear productos con diferentes valores de RAM y marcas.
        Act: Realizar petición GET al endpoint de opciones de filtro.
        Assert: Retornar 200 OK y verificar que las listas (brands, ram) no estén vacías.
        """
        brand = BrandFactory(name="Apple")
        ProductFactory(brand=brand, ram=8, storage=128)
        ProductFactory(ram=12, storage=256)

        url = reverse('products:product-filters')

        print("\nTest 3: Realizar petición GET al endpoint de opciones de filtro")

        response = api_client.get(url)

        print(f"DEBUG: Respuesta: {response.status_code}")

        assert response.status_code == status.HTTP_200_OK
        assert "brands" in response.data
        assert "ram" in response.data
        assert 8 in response.data['ram']
        assert 12 in response.data['ram']
        assert any(b['name'] == "Apple" for b in response.data['brands'])


@pytest.mark.django_db
class TestDependenciesViewSets:
    """Tests rápidos para verificar que los catálogos funcionan"""

    def test_list_brands_success(self, api_client):
        """
        Arrange: Crear 2 marcas.
        Act: GET a brands-list.
        Assert: Retornar 200 y 2 elementos.
        """
        BrandFactory.create_batch(2)
        url = reverse('products:brand-list')

        print("\nTest 4: Crear 2 marcas.")

        response = api_client.get(url)

        print(f"DEBUG: Respuesta: {response.status_code}")
        print(f"DEBUG: Lista de brands: {response.data}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
