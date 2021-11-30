from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from configuracion.views import ConfiguraiconView, ConfiguracionSearchViewSet, configuracion_lista_sin_paginacion

router = routers.DefaultRouter()
router.register(r'configuracion', ConfiguraiconView, basename='configuracion')

urlpatterns = [
    path('', include(router.urls)),
    path('busqueda/', ConfiguracionSearchViewSet.as_view({'get': 'list'}), name='busqueda-configuracion'),
    path('configuracion-lista/', configuracion_lista_sin_paginacion, name='listado_configuracion')
]
