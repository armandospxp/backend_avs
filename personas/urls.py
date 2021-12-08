# django
from django.urls import path
# rest-framework
from rest_framework.urlpatterns import format_suffix_patterns
# views de Personas
from personas.views import PersonaList, PerosnaDetail, PersonaProveedorList, PersonaClienteList, PersonaSearchViewSet, \
    PersonaProveedorSearchViewSet, personas_lista_sin_paginacion

"""Urls de personas"""
urlpatterns = format_suffix_patterns([
    path('', PersonaList.as_view(), name='personas'),
    path('<int:pk>/', PerosnaDetail.as_view(), name='persona_detail'),
    path('busqueda/', PersonaSearchViewSet.as_view({'get': 'list'}), name='personasearch'),
    path('busquedaproveedor/', PersonaProveedorSearchViewSet.as_view({'get': 'list'}), name='personaproveedorsearch'),
    path('proveedores/', PersonaProveedorList.as_view(), name='personaempleado'),
    path('clientes/', PersonaClienteList.as_view(), name='personaproveedor'),
    path('clientes-lista/', personas_lista_sin_paginacion, name='lista-clientes')
])
