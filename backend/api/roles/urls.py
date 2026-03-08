from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.roles.views import RolesViewSet

app_name = "roles"

router = DefaultRouter()
router.register(r'', RolesViewSet, basename='roles')

urlpatterns = [
    path('', include(router.urls)),
]
