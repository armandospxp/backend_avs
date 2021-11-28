from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from configuracion.views import ConfiguraiconView

router = routers.DefaultRouter()
router.register(r'configuracion', ConfiguraiconView, basename='configuracion')

urlpatterns = [
    path('', include(router.urls)),
]
