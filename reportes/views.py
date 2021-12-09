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
        query = Articulo.objects.all().values('id_articulo', 'codigo_barras', 'stock_minimo', 'stock_actual', 'nombre').order_by(
            'id_articulo')
        serializer = ReporteListaArticulosStock(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReporteTotaldeCompras(viewsets.GenericViewSet):
    """Vista para la suma total de compras hechas"""

    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        # total_factura_compra = FacturaCompra.objects.filter(estado='A').sum('total')
        query = "select sum(f.total) from public.facturas_facturacompra f where f.estado='A';"
        # factura_compra = FacturaCompra.objects.raw(query)
        with connection.cursor() as cursor:
            cursor.execute(query)
            suma = cursor.fetchone()
            respuesta = {'total_compras': suma[0]}
        cursor.close()
        return Response(respuesta, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        fecha_inicio = str(data['fecha_inicio'])
        fecha_fin = str(data['fecha_fin'])
        query = "select sum(f.total) from public.facturas_facturacompra f where f.estado='A' and f.fecha_creacion between %s and %s;"
        with connection.cursor() as cursor:
            cursor.execute(query, [fecha_inicio, fecha_fin])
            suma = cursor.fetchone()
            respuesta = {'total_compras': suma[0]}
            cursor.close()
        return Response(respuesta, status=status.HTTP_200_OK)


class ReporteTotaldeVentas(viewsets.GenericViewSet):
    """Vista para la suma total de ventas hechas"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = "select sum(v.total) from public.ventas_venta v where v.estado='A';"
        with connection.cursor() as cursor:
            cursor.execute(query)
            suma = cursor.fetchone()
            respuesta = {'total_ventas': suma[0]}
        cursor.close()
        return Response(respuesta, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        fecha_inicio = str(data['fecha_inicio'])
        fecha_fin = str(data['fecha_fin'])
        query = "select sum(v.total) from public.ventas_venta v where v.estado='A' and v.fecha between %s and %s;"
        with connection.cursor() as cursor:
            cursor.execute(query, [fecha_inicio, fecha_fin])
            suma = cursor.fetchone()
            respuesta = {'total_ventas': suma[0]}
            cursor.close()
        return Response(respuesta, status=status.HTTP_200_OK)


class ReporteVendedorMayorVenta(viewsets.GenericViewSet):
    """Vista para el vendedor con mayor numero de ventas"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = "select u.id, u.first_name||' '||u.last_name nombre_apellido, sum(v.total) total from public.users_user u join public.ventas_venta v on v.id_usuario_id = u.id where v.estado='A' group by u.id order by total desc;"
        with connection.cursor() as cursor:
            cursor.execute(query)
            vendedor = cursor.fetchone()
            respuesta = {'id': vendedor[0],
                         'nombre_vendedor': vendedor[1],
                         'ventas_totales': vendedor[2]}
            cursor.close()
        return Response(respuesta, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        query = "select distinct u.id, u.first_name||' '||u.last_name nombre_apellido, sum(v.total) total from public.users_user u join public.ventas_venta v on v.id_usuario_id = u.id where v.estado='A' and v.fecha between %s and %s group by u.id order by total desc;"
        data = request.data
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        with connection.cursor() as cursor:
            cursor.execute(query, [fecha_inicio, fecha_fin])
            vendedor = cursor.fetchone()
            respuesta = {'id': vendedor[0],
                         'nombre_vendedor': vendedor[1],
                         'ventas_totales': vendedor[2]}
            cursor.close()
        return Response(respuesta, status=status.HTTP_200_OK)


class ReporteArticulosMasVendidosSql(viewsets.GenericViewSet):
    """Vista para la suma total de los articulos que mas se vendio"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = "select ar.nombre nombre_articulo, count(dt.id_articulo_id) cantidad from ventas_detalleventa dt join articulos_articulo ar on dt.id_articulo_id = ar.id_articulo join ventas_venta_id_detalle_venta it on it.detalleventa_id = dt.id_detalle_venta join ventas_venta v on v.id_venta = it.venta_id where v.estado='A' group by ar.nombre  order by cantidad desc;"
        a = []
        cursor = connection.cursor()
        cursor.execute(query)
        articulos = cursor.fetchall()
        for row in articulos:
            respuesta = {'nombre_articulo': row[0],
                         'cantidad': row[1]}
            a.append(respuesta)
        cursor.close()
        return Response(a, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        query = "select ar.nombre nombre_articulo, count(dt.id_articulo_id) cantidad from ventas_detalleventa dt join articulos_articulo ar on dt.id_articulo_id = ar.id_articulo join ventas_venta_id_detalle_venta it on it.detalleventa_id = dt.id_detalle_venta join ventas_venta v on v.id_venta = it.venta_id where v.estado='A' and v.fecha between %s and %s group by ar.nombre  order by cantidad desc;"
        data = request.data
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        a = []
        cursor = connection.cursor()
        cursor.execute(query, [fecha_inicio, fecha_fin])
        articulos = cursor.fetchall()
        for row in articulos:
            respuesta = {'nombre_articulo': row[0],
                         'cantidad': row[1]}
            a.append(respuesta)
        cursor.close()
        return Response(a, status=status.HTTP_200_OK)


class ReporteVendedoresVentasSql(viewsets.GenericViewSet):
    """Vista para la suma total de los vendedores con las ventas que mas se vendio"""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = "select u.id, u.first_name||' '||u.last_name nombre_apellido, sum(v.total) total from public.users_user u join public.ventas_venta v on v.id_usuario_id = u.id where v.estado='A' group by u.id order by total desc;"
        a = []
        cursor = connection.cursor()
        cursor.execute(query)
        articulos = cursor.fetchall()
        for row in articulos:
            respuesta = {'id': row[0],
                         'nombre_apellido': row[1],
                         'total': row[2]}
            a.append(respuesta)
        cursor.close()
        return Response(a, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        query = "select u.id, u.first_name||' '||u.last_name nombre_apellido, sum(v.total) total from public.users_user u join public.ventas_venta v on v.id_usuario_id = u.id where v.estado='A' and v.fecha between %s and %s group by u.id order by total desc;"
        data = request.data
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        a = []
        cursor = connection.cursor()
        cursor.execute(query, [fecha_inicio, fecha_fin])
        articulos = cursor.fetchall()
        for row in articulos:
            respuesta = {'id': row[0],
                         'nombre_apellido': row[1],
                         'total': row[2]}
            a.append(respuesta)
        cursor.close()
        return Response(a, status=status.HTTP_200_OK)
