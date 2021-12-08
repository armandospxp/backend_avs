# django
from django.urls import path, include
# rest-framework
from rest_framework import routers
# vistas de nota de credito
from nota_credito import views as nota_credito_views
from nota_credito.views import NotaCreditoVentaSearchViewSet, NotaCreditoProveedorSearchViewSet

"""Los router son herramientas para crear dinamicamente los urls de nota de credito"""
router = routers.DefaultRouter()
router.register(r'nota-credito-venta', nota_credito_views.NotaCreditoVentaView, basename='nota-credito-venta')
router.register(r'detalle-nota-credito-venta', nota_credito_views.DetalleNotaCreditoVentaView, 'detalle-nota-credito-venta')
router.register(r'nota-credito-proveedor', nota_credito_views.NotaCreditoProveedorView, basename='nota-credito-proveedor')
router.register(r'detalle-nota-credito-proveedor', nota_credito_views.DetalleNotaCreditoProveedorView, basename='detalle-nota-credito-proveedor')


"""Urls de Nota de Credito"""
urlpatterns = [
    path('', include(router.urls)),
    path('busqueda/', NotaCreditoVentaSearchViewSet.as_view({'get': 'list'}), name='busqueda-nota-credito'),
    path('busqueda-nota-credito-proveedor/', NotaCreditoProveedorSearchViewSet.as_view({'get': 'list'}), name='busqueda-nota-credito-proveedor'),
]
