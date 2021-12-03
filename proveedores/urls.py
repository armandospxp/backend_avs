from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from proveedores.views import ProveedorList, ProveedorSearchViewSet, ProveedorDetail, proveedores_lista_sin_paginacion

urlpatterns = format_suffix_patterns([
    path('', ProveedorList.as_view(), name='proveedores'),
    path('<int:pk>/', ProveedorDetail.as_view(), name='proveedores_detail'),
    path('busqueda/', ProveedorSearchViewSet.as_view({'get': 'list'}), name='proveedoressearch'),
    path('proveedores-lista/', proveedores_lista_sin_paginacion, name='lista-proveedores')
])
