# django
from django.urls import path, include
# vistas de ventas
from ventas import views as ventas_views
# rest-framework
from rest_framework import routers
# vista particulares de datos de factrua y busqueda de ventas
from ventas.views import datos_factura_venta, VentaSearchViewSet

# router es un metodo de registrar dinamicamente las rutas de acceso a las vistas
router = routers.DefaultRouter()
router.register(r'ventas', ventas_views.VentaView, basename='ventas')
router.register(r'detalle-ventas', ventas_views.DetalleVentaView, 'detalle-ventas')

# urls de ventas
urlpatterns = [
    path('', include(router.urls)),
    path('factura/<int:id_venta>/', datos_factura_venta, name='factura'),
    path('busqueda/', VentaSearchViewSet.as_view({'get': 'list'}), name='busqueda-ventas'),
]
