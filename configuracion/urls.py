# django
from django.urls import path, include
# rest-framework
from rest_framework import routers
# vistas de configuracion
from configuracion.views import ConfiguraiconView, ConfiguracionSearchViewSet, configuracion_lista_sin_paginacion

"""Con routers se asigna dinamicamente los urls"""
router = routers.DefaultRouter()
router.register(r'configuracion', ConfiguraiconView, basename='configuracion')

"""Urls de configuracion"""
urlpatterns = [
    path('', include(router.urls)),
    path('busqueda/', ConfiguracionSearchViewSet.as_view({'get': 'list'}), name='busqueda-configuracion'),
    path('configuracion-lista/', configuracion_lista_sin_paginacion, name='listado_configuracion')
]
