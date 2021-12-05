import pdb

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from articulos.models import Articulo
from facturas.models import FacturaCompra
from nota_credito.models import NotaCreditoCliente, DetalleNotaCredito, NotaCreditoProveedor, \
    DetalleNotaCreditoProveedor
from nota_credito.serializers import NotaCreditoVentaModelSerializer, DetalleNotaCreditoVentaModelSerializer, \
    DetalleNotaCreditoProveedorModelSerializer, NotaCreditoProveedorModelSerializer
from ventas.models import Venta


# from nota_credito.serializers import AUX


class NotaCreditoVentaView(viewsets.ModelViewSet):
    serializer_class = NotaCreditoVentaModelSerializer
    queryset = NotaCreditoCliente.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        nota_credito_cliente = NotaCreditoCliente.objects.filter(estado='A').order_by('-id_nota_credito_cliente')
        return nota_credito_cliente

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = NotaCreditoVentaModelSerializer(data=data)
        if serializer.is_valid():
            pdb.set_trace()
            serializer.save()
            datos = dict(serializer.data)
            id_venta = int(datos['id_venta'])
            monto_total = int(datos['monto_total'])
            venta = get_object_or_404(Venta.objects.all(), pk=id_venta)
            if venta.total_nota_credito <= venta.total:
                venta.total_nota_credito = venta.total_nota_credito + monto_total
                venta.save()
            else:
                raise status.HTTP_400_BAD_REQUEST
            nota_credito_cliente = NotaCreditoCliente.objects.latest('id_nota_credito_cliente')
            detalle_nota_credito = DetalleNotaCredito.objects.filter(notacreditocliente=nota_credito_cliente)
            for detalle in detalle_nota_credito:
                cantidad = int(detalle.cantidad)
                id_articulo = int(detalle.id_articulo.id_articulo)
                articulo = get_object_or_404(Articulo.objects.all(), pk=id_articulo)
                articulo.stock_actual = articulo.stock_actual + cantidad
                articulo.save()
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


class NotaCreditoVentaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = NotaCreditoCliente.objects.filter()
    serializer_class = NotaCreditoVentaModelSerializer
    search_fields = ['id_nota_credito_cliente',
                     'id_venta__id_detalle_venta__id_articulo__nombre',
                     'id_venta__id_detalle_venta__id_articulo__codigo_barras',
                     'id_venta__id_cliente__nombre_apellido']


class NotaCreditoProveedorView(viewsets.ModelViewSet):
    serializer_class = NotaCreditoProveedorModelSerializer
    queryset = NotaCreditoProveedor.objects.filter(estado='A').order_by('-id_nota_credito_proveedor')
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = NotaCreditoProveedorModelSerializer(data=data)
        if serializer.is_valid():
            nota_credito_proveedor = NotaCreditoProveedor.objects.latest('id_nota_credito_proveedor')
            pk_factura_compra = nota_credito_proveedor.id_factura_compra.pk
            factura_compra = get_object_or_404(FacturaCompra.objects.all(), pk=pk_factura_compra)
            if nota_credito_proveedor.monto_total <= factura_compra.total and factura_compra.total_nota_credito<= factura_compra.total:
                factura_compra.total_nota_credito = factura_compra.total_nota_credito + nota_credito_proveedor.monto_total
                factura_compra.save()
                serializer.save()
            else:
                error = {"error": "No el monto de nota de credito excede al monto total de compra de la factura"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            detalle_nota_credito_proveedor = DetalleNotaCreditoProveedor.objects.filter(notacreditoproveedor=nota_credito_proveedor)
            for detalle in detalle_nota_credito_proveedor:
                cantidad = int(detalle.cantidad)
                id_articulo = int(detalle.id_articulo.id_articulo)
                articulo = get_object_or_404(Articulo.objects.all(), pk=id_articulo)
                articulo.stock_actual = articulo.stock_actual - cantidad
                articulo.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = 'H'
        instance.save()
        detalle_nota_credito_proveedor = DetalleNotaCreditoProveedor.objects.filter(notacreditoproveedor=instance.pk)
        for detalle in detalle_nota_credito_proveedor:
            cantidad = int(detalle.cantidad)
            id_articulo = int(detalle.id_articulo.id_articulo)
            articulo = get_object_or_404(Articulo, pk=id_articulo)
            articulo.stock_actual = articulo.stock_actual + cantidad
            articulo.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetalleNotaCreditoProveedorView(viewsets.ModelViewSet):
    serializer_class = DetalleNotaCreditoProveedorModelSerializer
    queryset = DetalleNotaCreditoProveedor.objects.filter(estado='A')
    permission_classes = [IsAuthenticated]


class NotaCreditoProveedorSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = NotaCreditoProveedor.objects.filter()
    serializer_class = NotaCreditoProveedorModelSerializer
    search_fields = ['id_nota_credito_proveedor',
                     'id_factura_compra__id_proveedor__propietario',
                     'fecha']
