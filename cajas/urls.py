from django.urls import path, include
from rest_framework import routers

from cajas.views import CajaView, ArqueoCajaView, MovimientoCajaView, CajaSearchViewSet, ArqueoCajaSearchViewSet, MovimientoCajaSearchViewSet

router = routers.DefaultRouter()
router.register(r'cajas', CajaView, basename='cajas')
router.register(r'arqueo-caja', ArqueoCajaView, 'arqueo_caja')
router.register(r'movimiento-caja', MovimientoCajaView, 'movimiento-caja')

urlpatterns = [
    path('', include(router.urls)),
    path('busqueda-caja/', CajaSearchViewSet.as_view({'get': 'list'}), name='busqueda-caja'),
    path('busqueda-arqueo/', ArqueoCajaSearchViewSet.as_view({'get': 'list'}), name='busqueda-arqueo'),
    path('busqueda-movimiento/', MovimientoCajaSearchViewSet.as_view({'get': 'list'}), name='busqueda-movimiento'),
    ]
