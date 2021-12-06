from django.urls import path

from reportes.views import ReporteArticulosMasVendidos

# router = routers.DefaultRouter()
# router.register(r'arqueo-caja', ArqueoCajaView, 'arqueo_caja')
# router.register(r'movimiento-caja', MovimientoCajaView, 'movimiento-caja')
# router.register(r'retiro-dinero-caja', RetiroDineroCajaView, 'retiro-dinero-caja')

urlpatterns = [
    path('reporte-articulos/', ReporteArticulosMasVendidos.as_view({'get': 'list'}), name='reporte-articulos'),
    ]
