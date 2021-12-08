# django
from django.urls import path, include
# vistas de facturas
from facturas import views as facturas_views
# rest-framework
from rest_framework import routers
# vistas de busqueda de facturas
from facturas.views import FacturaCompraSearchViewSet

"""Los routers sirven para crear dinamicamente los urls"""
router = routers.DefaultRouter()
router.register(r'factura-compra', facturas_views.FacturaCompraView, basename='factura-compra')
router.register(r'detalle-factura-compra', facturas_views.DetalleFacturaCompraView, 'detalle-factura-compra')

"""Urls de Facturas"""
urlpatterns = [
    path('', include(router.urls)),
    path('busqueda/', FacturaCompraSearchViewSet.as_view({'get': 'list'}), name='busqueda-factura-compra'),
]
