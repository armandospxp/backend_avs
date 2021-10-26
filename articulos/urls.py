from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from articulos.views import ArticuloList, ArticuloDetail, ArticuloSearchViewSet, MarcaSearchViewSet, articulos_lista_sin_paginacion

urlpatterns = format_suffix_patterns([
    path('', ArticuloList.as_view(), name='articulos'),
    path('<int:pk>/', ArticuloDetail.as_view(), name='articulo'),
    path('busqueda/', ArticuloSearchViewSet.as_view({'get': 'list'}), name='busqueda-articulo'),
    path('marca/busqueda/', MarcaSearchViewSet.as_view({'get': 'list'}), name='busqueda-marca'),
    path('articulos-lista/', articulos_lista_sin_paginacion, name='listado_articulos')
])
