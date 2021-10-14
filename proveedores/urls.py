from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from proveedores.views import ProveedorList, ProveedorSearchViewSet, ProveedorDetail

urlpatterns = format_suffix_patterns([
    path('', ProveedorList.as_view(), name='proveedores'),
    path('<int:pk>/', ProveedorDetail.as_view(), name='proveedores_detail'),
    path('busqueda/', ProveedorSearchViewSet.as_view({'get': 'list'}), name='proveedoressearch'),
])
