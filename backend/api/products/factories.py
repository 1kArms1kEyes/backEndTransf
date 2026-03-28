import factory

from ..products.models import Product, Brand, Color, MaxSupportNetwork, OperatingSystem


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker('company')


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Color

    name = factory.Faker('color_name')


class NetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MaxSupportNetwork

    name = factory.Iterator(['4G', '5G', '6G'])


class OSFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OperatingSystem

    name = factory.Faker('word')


# Fábrica de Producto (con todos los campos obligatorios)
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('bothify', text='Phone-##??')
    storage = factory.Faker('random_element', elements=[64, 128, 256, 512])
    ram = factory.Faker('random_element', elements=[4, 8, 12, 16])
    release_date = factory.Faker('date_this_decade')
    max_battery = factory.Faker('random_int', min=3000, max=5500)
    main_camera_res = factory.Faker('pyfloat', left_digits=2, right_digits=1, positive=True, min_value=12.0)
    selfie_camera_res = factory.Faker('pyfloat', left_digits=2, right_digits=1, positive=True, min_value=8.0)
    has_nfc = factory.Faker('boolean')
    has_headphone_jack = factory.Faker('boolean')
    synopsis = factory.Faker('paragraph', nb_sentences=3)

    brand = factory.SubFactory(BrandFactory)
    color = factory.SubFactory(ColorFactory)
    max_supported_network = factory.SubFactory(NetworkFactory)
    operating_system = factory.SubFactory(OSFactory)

    product_image = None
