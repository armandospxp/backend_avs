from django.urls import path, include
from ventas.views import VentaView, DetalleVentaView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ventas', VentaView)
router.register('detalle-ventas', DetalleVentaView)