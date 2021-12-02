from django.urls import path, include

from facturas import views as facturas_views

from rest_framework import routers

from facturas.views import FacturaCompraSearchViewSet

router = routers.DefaultRouter()
router.register(r'factura-compra', facturas_views.FacturaCompraView, basename='factura-compra')
router.register(r'detalle-factura-compra', facturas_views.DetalleFacturaCompraView, 'detalle-factura-compra')

urlpatterns = [
    path('', include(router.urls)),
    path('busqueda/', FacturaCompraSearchViewSet.as_view({'get': 'list'}), name='busqueda-factura-compra'),
]