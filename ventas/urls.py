from django.urls import path, include
from ventas import views as ventas_views
from ventas.reports import imprimir_factura_venta
from rest_framework import routers, urlpatterns

from ventas.views import datos_factura_venta, VentaSearchViewSet

router = routers.DefaultRouter()
router.register(r'ventas', ventas_views.VentaView, basename='ventas')
router.register(r'detalle-ventas', ventas_views.DetalleVentaView, 'detalle-ventas')

urlpatterns = [
    path('', include(router.urls)),
    path('factura/<int:id_venta>/', datos_factura_venta, name='factura'),
    path('busqueda/', VentaSearchViewSet.as_view({'get': 'list'}), name='busqueda-ventas'),
]