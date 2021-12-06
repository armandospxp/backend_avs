from django.urls import path

from reportes.views import ReporteArticulosMasVendidos, ReporteTopVendedores, ReporteCantidadVendidaDia, ReporteCantidadVendidaMes

urlpatterns = [
    path('reporte-articulos/', ReporteArticulosMasVendidos.as_view({'get': 'list'}), name='reporte-articulos'),
    path('reporte-vendedores/', ReporteTopVendedores.as_view({'get': 'list'}), name='reporte-vendedores'),
    path('reporte-ventas-dia/', ReporteCantidadVendidaDia.as_view({'get': 'list'}), name='reporte-ventas-dia'),
    path('reporte-ventas-mes/', ReporteCantidadVendidaMes.as_view({'get': 'list'}), name='reporte-ventas-mes'),
    ]
