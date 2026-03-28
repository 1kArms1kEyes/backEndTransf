import factory

from .models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    comment = factory.Faker('sentence')
    user = factory.SubFactory('api.users.factories.UserFactory')
    product = factory.SubFactory('api.products.factories.ProductFactory')
