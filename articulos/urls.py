# django
from django.urls import path
# rest-framework
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
# vistas de articulos
from articulos.views import ArticuloList, ArticuloDetail, ArticuloSearchViewSet, MarcaSearchViewSet, \
    articulos_lista_sin_paginacion, AjusteStockView, AjusteStockSearchViewSet

"""Los routers sirven para crear dinamicamente los urls de articulos"""
router = routers.DefaultRouter()
router.register(r'ajuste-stock', AjusteStockView, basename='ajuste-stock')

"""Urls de articulos"""
urlpatterns = format_suffix_patterns([
    path('', ArticuloList.as_view(), name='articulos'),
    path('<int:pk>/', ArticuloDetail.as_view(), name='articulo'),
    path('busqueda/', ArticuloSearchViewSet.as_view({'get': 'list'}), name='busqueda-articulo'),
    path('marca/busqueda/', MarcaSearchViewSet.as_view({'get': 'list'}), name='busqueda-marca'),
    path('articulos-lista/', articulos_lista_sin_paginacion, name='listado_articulos'),
    path('ajuste-stock/', AjusteStockView.as_view({
        'get': 'retrieve',
        'get': 'list',
        'post': 'create',
        'delete': 'destroy'
    })),
    path('busqueda-ajuste/', AjusteStockSearchViewSet.as_view({'get': 'list'}), name='busqueda-ajuste-stock')
])
