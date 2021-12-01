from django.urls import path, include
from rest_framework import routers

from nota_credito import views as nota_credito_views

router = routers.DefaultRouter()
router.register(r'nota-credito-venta', nota_credito_views.NotaCreditoVentaView, basename='nota-credito-venta')
router.register(r'detalle-nota-credito-venta', nota_credito_views.DetalleNotaCreditoVentaView, 'detalle-nota-credito-venta')

urlpatterns = [
    path('', include(router.urls)),
]