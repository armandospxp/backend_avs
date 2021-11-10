import pdb
from datetime import datetime
from io import BytesIO

from django.http import response, HttpResponse
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from articulos.models import Articulo
from ventas.models import DetalleVenta, Venta
from ventas.serializers import VentaModelSerializer, DetalleVentaModelSerializer
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404


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

    def get_queryset(self):
        venta = Venta.objects.all()
        return venta

    def create(self, request, *args, **kwargs):
        # nueva_venta = Venta.objects.create(id_venta=data["id_venta"], id_cliente=data["id_cliente"], fecha=data['fecha'], hora=data['hora'])
        # nueva_venta.save()
        serializer = VentaModelSerializer(data=request.data)
        # id_detalle_venta = request['id_detalle_venta']
        # detalle_serializer = DetalleVentaModelSerializer(id_detalle_venta)
        # if detalle_serializer.is_valid():
        #     detalle_serializer.save()
        data = request.data
        cliente = data.get('id_cliente')
        if cliente is not None:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalleVentaView(viewsets.ModelViewSet):
    serializer_class = DetalleVentaModelSerializer
    queryset = DetalleVenta.objects.all()

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
        detalle_venta = get_object_or_404(queryset, pk)
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
