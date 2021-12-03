from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from facturas.models import DetalleFacturaCompra, FacturaCompra
from facturas.serializers import FacturaCompraModelSerializer, DetalleFacturaCompraModelSerializer


class FacturaCompraView(viewsets.ModelViewSet):
    """
        ViewSet de Factura Compra
        """
    serializer_class = FacturaCompraModelSerializer
    queryset = FacturaCompra.objects.filter(estado='A')
    permission_classes = [IsAuthenticated]


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
