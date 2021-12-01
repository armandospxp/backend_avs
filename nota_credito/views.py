import pdb

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from articulos.models import Articulo
from nota_credito.models import NotaCreditoCliente, DetalleNotaCredito
from nota_credito.serializers import NotaCreditoVentaModelSerializer, DetalleNotaCreditoVentaModelSerializer
from ventas.models import Venta


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


class NotaCreditoVentaView(viewsets.ModelViewSet):
    serializer_class = NotaCreditoVentaModelSerializer
    queryset = NotaCreditoCliente.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        nota_credito_cliente = NotaCreditoCliente.objects.filter(estado='A').order_by('-id_nota_credito_cliente')
        return nota_credito_cliente

    def create(self, request, *args, **kwargs):
        data = request.data
        detalle_nota_credito = data.get('id_detalle_nota_credito')
        serializer = NotaCreditoVentaModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            datos = dict(serializer.data)
            id_venta = int(datos['id_venta'])
            monto_total = int(datos['monto_total'])
            venta = get_object_or_404(Venta.objects.all(), pk=id_venta)
            venta.total = venta.total - monto_total
            venta.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalleNotaCreditoVentaView(viewsets.ModelViewSet):
    serializer_class = DetalleNotaCreditoVentaModelSerializer
    queryset = DetalleNotaCredito.objects.all()

    def get_queryset(self):
        detalle_nota_credito = DetalleNotaCredito.objects.all()
        return detalle_nota_credito

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = DetalleNotaCreditoVentaModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            datos = serializer.data
            id_detalle_nota_credito = datos['id_detalle_nota_credito']
            pdb.set_trace()
            detalle_nota_credito = get_object_or_404(DetalleNotaCredito.objects.all(), pk=id_detalle_nota_credito)
            for detalle in detalle_nota_credito:
                id_articulo = detalle.id_articulo
                articulo = get_object_or_404(Articulo.objects.all(), pk=id_articulo)
                cantidad = detalle.cantidad
                articulo.stock_actual = articulo.stock_actual + cantidad
                articulo.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
