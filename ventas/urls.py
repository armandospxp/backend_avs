from django.urls import path, include
from ventas.views import Venta, DetalleVenta
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ventas', Venta)
router.register('detalle-ventas', DetalleVenta)