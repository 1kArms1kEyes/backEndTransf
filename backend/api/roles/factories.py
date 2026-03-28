import factory

from .models import (Role)


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = 'Admin'
