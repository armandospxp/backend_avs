import pdb

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from articulos.models import Articulo
from facturas.models import DetalleFacturaCompra, FacturaCompra
from facturas.serializers import FacturaCompraModelSerializer, DetalleFacturaCompraModelSerializer


class FacturaCompraView(viewsets.ModelViewSet):
    """
        ViewSet de Factura Compra
        """
    serializer_class = FacturaCompraModelSerializer
    queryset = FacturaCompra.objects.filter(estado='A')
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            factura_compra = FacturaCompra.objects.latest('id_factura_compra')
            detalle_factura_compra = DetalleFacturaCompra.objects.filter(facturacompra=factura_compra.pk)
            # detalle_factura_compra = DetalleFacturaCompra.objects.latest('id_detalle_factura_compra')
            for detalle in detalle_factura_compra:
                cantidad = int(detalle.cantidad)
                id_articulo = int(detalle.id_articulo.id_articulo)
                articulo = get_object_or_404(Articulo, pk=id_articulo)
                articulo.stock_actual = articulo.stock_actual + cantidad
                articulo.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = 'H'
        instance.save()
        detalle_factura_compra = DetalleFacturaCompra.objects.filter(facturacompra=instance.pk)
        for detalle in detalle_factura_compra:
            cantidad = int(detalle.cantidad)
            id_articulo = int(detalle.id_articulo.id_articulo)
            articulo = get_object_or_404(Articulo, pk=id_articulo)
            articulo.stock_actual = articulo.stock_actual - cantidad
            articulo.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetalleFacturaCompraView(viewsets.ModelViewSet):
    serializer_class = DetalleFacturaCompraModelSerializer
    queryset = DetalleFacturaCompra.objects.filter(estado='A')
    permission_classes = [IsAuthenticated]


class FacturaCompraSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = FacturaCompra.objects.filter()
    serializer_class = FacturaCompraModelSerializer
    search_fields = ['id_factura_compra',
                     'numero_factura',
                     'id_proveedor__propietario']
