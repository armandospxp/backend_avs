from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from personas.views import PersonaList, PerosnaDetail, PersonaProveedorList, PersonaClienteList
    # , PersonaSearchViewSet

urlpatterns = format_suffix_patterns([
    path('', PersonaList.as_view(), name='personas'),
    path('<int:pk>/', PerosnaDetail.as_view(), name='persona_detail'),
    # path('busqueda/', PersonaSearchViewSet, name='personasearch'),
    path('clientes/', PersonaProveedorList.as_view(), name='personaempleado'),
    path('proveedores/', PersonaClienteList.as_view(), name='personaproveedor'),
])
