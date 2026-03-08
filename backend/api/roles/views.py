from rest_framework.viewsets import ModelViewSet

from api.roles.models import Role
from api.roles.serializers import RoleSerializer


class RolesViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
