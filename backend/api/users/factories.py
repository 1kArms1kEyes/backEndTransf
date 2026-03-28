import factory

from ..users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.Faker('email')
    role = factory.SubFactory('api.roles.factories.RoleFactory')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop('password', 'password123')
        obj = model_class(*args, **kwargs)
        obj.set_password(password)
        obj.save()
        return obj
