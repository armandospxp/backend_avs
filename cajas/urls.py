from django.urls import path, include
from rest_framework import routers

from cajas.views import ArqueoCajaView, MovimientoCajaView, ArqueoCajaSearchViewSet, MovimientoCajaSearchViewSet, \
    RetiroDineroCajaView

router = routers.DefaultRouter()
router.register(r'arqueo-caja', ArqueoCajaView, 'arqueo_caja')
router.register(r'movimiento-caja', MovimientoCajaView, 'movimiento-caja')
router.register(r'retiro-dinero-caja', RetiroDineroCajaView, 'retiro-dinero-caja')

urlpatterns = [
    path('', include(router.urls)),
    path('busqueda-arqueo/', ArqueoCajaSearchViewSet.as_view({'get': 'list'}), name='busqueda-arqueo'),
    path('busqueda-movimiento/', MovimientoCajaSearchViewSet.as_view({'get': 'list'}), name='busqueda-movimiento'),
    ]
