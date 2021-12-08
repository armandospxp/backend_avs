# django
from django.urls import path

# app de reportes
from reportes.views import ReporteArticulosMasVendidos, ReporteTopVendedores, ReporteCantidadVendidaDia, \
    ReporteCantidadVendidaMes, ReporteStockActualMinimoArtiuclos, ReporteTotaldeCompras, ReporteTotaldeVentas, \
    ReporteVendedorMayorVenta, ReporteArticulosMasVendidosSql

"""Urls de reportes"""
urlpatterns = [
    path('reporte-articulos/', ReporteArticulosMasVendidos.as_view({'get': 'list'}), name='reporte-articulos'),
    path('reporte-vendedores/', ReporteTopVendedores.as_view({'get': 'list'}), name='reporte-vendedores'),
    path('reporte-ventas-dia/', ReporteCantidadVendidaDia.as_view({'get': 'list'}), name='reporte-ventas-dia'),
    path('reporte-ventas-mes/', ReporteCantidadVendidaMes.as_view({'get': 'list'}), name='reporte-ventas-mes'),
    path('reporte-total-compras/', ReporteTotaldeCompras.as_view({'get': 'list'}), name='reporte-compras-total'),
    path('reporte-total-ventas/', ReporteTotaldeVentas.as_view({'get': 'list'}), name='reporte-compras-total'),
    path('reporte-mejor-vendedor/', ReporteVendedorMayorVenta.as_view({'get': 'list'}), name='reporte-compras-total'),
    path('reporte-cantidad-articulos-vendidos/', ReporteArticulosMasVendidosSql.as_view({'get': 'list'}), name='reporte-compras-total'),
    path('reporte-articulos-stock/', ReporteStockActualMinimoArtiuclos.as_view({'get': 'list'}), name='reporte-articulos-stock'),
    ]
