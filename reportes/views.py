# python datetime
import pdb
from datetime import date, timedelta
# django
from django.db.models import Sum, Count
from django.db import connection
# rest-framework
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# modelo articulos
from articulos.models import Articulo
# serializador de reportes
from reportes.serializers import ReporteArticulosVendidos, ReporteTopVendendores, ReporteListaArticulosStock
# modelo de factura compra
from facturas.models import FacturaCompra
# modelo de ventas
from ventas.models import DetalleVenta, Venta


class ReporteArticulosMasVendidos(viewsets.GenericViewSet):
    """Vista de reporte de articulos mas vendidos"""

    permission_classes = [IsAuthenticated]
    serializer_class = ReporteArticulosVendidos

    def list(self, request):
        query = DetalleVenta.objects.filter(estado='A').values('id_articulo__nombre', 'sub_total').annotate(
            total=Sum('sub_total')).annotate(cantidad_vendida=Count('id_articulo__nombre')).order_by(
            '-cantidad_vendida')[:5]
        serializer = ReporteArticulosVendidos(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReporteTopVendedores(viewsets.GenericViewSet):
    """ Vista de top vendedores y cantidades de ventas hechas"""

    permission_classes = [IsAuthenticated]
    serializer_class = ReporteTopVendendores

    def list(self, request):
        query = Venta.objects.filter(estado='A').values('id_usuario__first_name', 'id_usuario__last_name').annotate(
            cantidad_vendida=Count('id_usuario__first_name')).order_by('-cantidad_vendida')[:5]
        serializer = ReporteTopVendendores(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReporteCantidadVendidaDia(viewsets.GenericViewSet):
    """ Vista de cantidad de ventas hechas en el dia"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = Venta.objects.all().filter(fecha=date.today()).filter(estado='A').count()
        dict_query = {'cantidad_ventas_dia': query}
        return Response(dict_query, status=status.HTTP_200_OK)


class ReporteCantidadVendidaMes(viewsets.GenericViewSet):
    """Vista de cantidad de ventas hechas desde principio de mes hasta ahora"""

    def list(self, request):
        query = Venta.objects.filter(
            fecha__range=(date.today() - timedelta(date.today().day + 1), date.today())).filter(estado='A').count()
        dict_query = {'cantidad_ventas_mes': query}
        return Response(dict_query, status=status.HTTP_200_OK)


class ReporteStockActualMinimoArtiuclos(viewsets.GenericViewSet):
    """Vista de stock actual y minimo de todos los articulos"""

    permission_classes = [IsAuthenticated]
    serializer_class = ReporteListaArticulosStock

    def list(self, request):
        query = Articulo.objects.all().values('id_articulo', 'codigo_barras', 'stock_minimo', 'stock_actual').order_by(
            'id_articulo')
        serializer = ReporteListaArticulosStock(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReporteTotaldeCompras(viewsets.GenericViewSet):
    """Vista para la suma total de compras hechas"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        # total_factura_compra = FacturaCompra.objects.filter(estado='A').sum('total')
        query = "select sum(f.total) from public.facturas_facturacompra f where f.estado='A';"
        # factura_compra = FacturaCompra.objects.raw(query)
        with connection.cursor() as cursor:
            cursor.execute(query)
            suma = cursor.fetchone()
            respuesta = {'total_compras': suma}
        return Response(respuesta, status=status.HTTP_200_OK)
