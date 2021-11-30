import pdb
from datetime import datetime, date
from io import BytesIO

from django.http import response, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from articulos.models import Articulo
from personas.models import Persona
from ventas.models import DetalleVenta, Venta
from ventas.serializers import VentaModelSerializer, DetalleVentaModelSerializer, VentaListModelSerializer
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from utilidades.numero_letras import numero_a_letras
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated


class MyPaginationMixin(object):
    pagination_class = PageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class VentaView(viewsets.ModelViewSet):
    serializer_class = VentaModelSerializer
    queryset = Venta.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        venta = Venta.objects.filter(estado='A').order_by('-id_venta')
        return venta

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = VentaListModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = VentaModelSerializer(data=request.data)
        data = request.data
        data['id_usuario'] = request.user
        cliente = data.get('id_cliente')
        if cliente is not None:
            if serializer.is_valid():
                serializer.save()
                respuesta = dict(serializer.data)
                url = 'avs-backend.herokuapp.com/ventas/factura/'
                pk = str(Venta.objects.last().id_venta)
                url_nueva = url + pk + '/'
                respuesta['factura'] = url_nueva
                # se agrega campo monto a letras y se envia el parametro del monto total
                respuesta['monto_letras'] = numero_a_letras(int(respuesta['total']))
                # pdb.set_trace()
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(respuesta, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Venta.objects.all()
        detalle_venta = get_object_or_404(queryset, pk=pk)
        detalle_venta.estado = 'H'
        detalle_venta.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetalleVentaView(viewsets.ModelViewSet):
    serializer_class = DetalleVentaModelSerializer
    queryset = DetalleVenta.objects.filter(estado='A')

    def get_queryset(self):
        detalle_venta = DetalleVenta.objects.all()
        return detalle_venta

    def create(self, request, *args, **kwargs):
        data = request.data
        cantidad = data.get('cantidad')
        pk_articulo = data.get('id_articulo')
        sub_total = actualizar_subtotal(pk_articulo, cantidad)
        datos_modificar = data.copy()
        datos_modificar['sub_total'] = sub_total
        serializer = DetalleVentaModelSerializer(data=datos_modificar)
        if serializer.is_valid():
            actualizar_stock(pk_articulo, 'V', cantidad)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = DetalleVenta.objects.all()
        detalle_venta = get_object_or_404(queryset, pk=pk)
        serializer = DetalleVentaModelSerializer(detalle_venta)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = DetalleVenta.objects.all()
        detalle_venta = get_object_or_404(queryset, pk=pk)
        detalle_venta.estado = 'H'
        detalle_venta.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        detalle_venta = self.get_object(pk)
        serializer = DetalleVentaModelSerializer(detalle_venta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def actualizar_stock(pk, estado, cantidad):
    """Procedimiento para descontar stock de articulo, de tal forma a que se vaya actualizando
    cada vez que se compra o vende.
    Dependiendo del estado, si es venta o reposicion, se restara o se sumara un articulo."""

    if estado == 'V':
        articulo = Articulo.objects.get(pk=pk)
        if articulo.stock_actual <= articulo.stock_minimo:
            raise HttpResponseNotAllowed
        else:
            stock_actual = articulo.stock_actual
            # articulo.objects.set(stock_actual=stock_actual - cantidad)
            articulo.stock_actual = int(articulo.stock_actual) - int(cantidad)
            articulo.save()


@api_view(('GET',))
def datos_factura_venta(request, id_venta):
    venta = Venta.objects.get(id_venta=id_venta)
    detalle_venta = venta.id_detalle_venta.filter()
    data = []
    articulo = []
    for art in detalle_venta:
        # pdb.set_trace()
        articulo.append({
            'codigo': str(art.id_articulo.codigo_barras),
            'cantidad': str(art.cantidad),
            'precio': str(art.id_articulo.precio_unitario),
            'iva': str(art.id_articulo.porc_iva),
            'sub_total': str(art.sub_total),
        })
    data.append({
        'fecha_emision': date.today(),
        'nombre_razon': str(venta.id_cliente.nombre_apellido),
        'direccion': str(venta.id_cliente.direccion),
        'condicion_venta': str(venta.tipo_factura),
        'ruc': str(venta.id_cliente.ruc),
        'total': str(venta.total),
        'total_letras': numero_a_letras(int(venta.total)),
        'detalle_venta': articulo,
    })
    # context = {
    #     'venta': VentaModelSerializer(venta),
    #     'detalle_venta': DetalleVentaModelSerializer(detalle_venta, many=True),
    #     'request': request,
    # }
    return Response(data)


def actualizar_subtotal(pk_articulo, cantidad):
    """Funcion para obtener el subtotal de un detalle_venta con respecto a un articulo especifico"""
    articulo = Articulo.objects.get(pk=pk_articulo)
    sub_total = (int(articulo.precio_unitario) * int(cantidad))
    return sub_total


def actualizar_total(pk, estado):
    """Procedimiento para actualizar el total de venta"""
    venta = Venta.objects.get(pk=pk)
    subtotal = 0
    if estado == 'S':
        venta.total = int(venta.total) + int(subtotal)
        venta.save()
