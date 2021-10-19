from django.urls import path, include
from ventas import views as ventas_views
from rest_framework import routers, urlpatterns

router = routers.DefaultRouter()
router.register(r'ventas', ventas_views.VentaView, basename='ventas')
router.register(r'detalle-ventas', ventas_views.DetalleVentaView, 'detalle-ventas')

urlpatterns = [
    path('', include(router.urls)),
]