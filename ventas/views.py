import pdb

from django.http import response
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
        data = request.data
        pk = data.get('id_cliente')
        # pdb.set_trace()
        if pk is not None:
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
        serializer = DetalleVentaModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = request.data
            pk = data.get('id_detalle_venta')
            actualizar_stock(pk, 'V')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = DetalleVenta.objects.all()
        detalle_venta = get_object_or_404(queryset, pk=pk)
        serializer = DetalleVentaModelSerializer(detalle_venta)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = DetalleVenta.objects.all()
        detalle_venta = get_object_or_404(queryset, pk)
        detalle_venta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        detalle_venta = self.get_object(pk)
        serializer = DetalleVentaModelSerializer(detalle_venta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def actualizar_stock(pk, estado):
    """Funcion para descontar stock de articulo, de tal forma a que se vaya actualizando 
    cada vez que se compra o vende.
    Dependiendo del estado, si es venta o reposicion, se restara o se sumara un articulo."""

    if estado == 'V':
        articulo = Articulo.objects.get(id=pk)
        if articulo.stock_minimo <= articulo.stock_actual:
            raise HttpResponseNotAllowed
        else:
            stock_actual = articulo.stock_actual
            articulo.objects.set(stock_actual=stock_actual - 1)
