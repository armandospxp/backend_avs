from django.http import response
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from articulos.models import Articulo
from ventas.models import DetalleVenta, Venta
from ventas.serializers import VentaModelSerializer, DetalleVentaModelSerializer
from django.http import HttpResponseNotAllowed

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
        data = request.data
        nueva_venta = Venta.objects.create(id_cliente=data["id_cliente"])
        serializer = VentaModelSerializer(nueva_venta)
        return Response(serializer.data)

class DetalleVentaView(viewsets.ModelViewSet):
    serializer_class = DetalleVentaModelSerializer
    queryset = DetalleVenta.objects.all()

    def get_queryset(self):
        detalle_venta = DetalleVenta.objects.all()
        return detalle_venta

    def create(self, request, *args, **kwargs):
        data = request.data
        nuevo_detalle_venta = DetalleVenta.objects.create(id_venta = data["id_venta"], id_articulo = data["id_articulo"], cantidad = data["cantidad"], subtotal=data["subtotal"], total=data["total"])
        serializer = DetalleVentaModelSerializer(nuevo_detalle_venta)
        descontar_stock(data["id_articulo"], 'V')
        return Response(serializer.data)


def descontar_stock(pk, estado):
    """Funcion para descontar stock de articulo, de tal forma a que se vaya actualizando cada vez que se compra o vende"""
    if estado == 'V':
        articulo = Articulo.objects.get(id=pk)
        if articulo.stock_minimo <= articulo.stock_actual:
            raise HttpResponseNotAllowed
        else:
            stock_actual = articulo.stock_actual
            articulo.objects.set(stock_actual=stock_actual - 1)