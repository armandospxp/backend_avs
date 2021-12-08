# django
from django.shortcuts import get_object_or_404
# rest-framework
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# modelo de articulos
from articulos.models import Articulo
# modelo de facturas
from facturas.models import DetalleFacturaCompra, FacturaCompra
# serializador de facturas
from facturas.serializers import FacturaCompraModelSerializer, DetalleFacturaCompraModelSerializer


class FacturaCompraView(viewsets.ModelViewSet):
    """
        ViewSet de Factura Compra
        """
    serializer_class = FacturaCompraModelSerializer
    queryset = FacturaCompra.objects.filter(estado='A').order_by('-id_factura_compra')
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Creacion de una factura compra"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            factura_compra = FacturaCompra.objects.latest('id_factura_compra')
            detalle_factura_compra = DetalleFacturaCompra.objects.filter(facturacompra=factura_compra.pk)
            for detalle in detalle_factura_compra:
                """Por cada articulo del detalle de la factura se actualiza su stock"""
                cantidad = int(detalle.cantidad)
                id_articulo = int(detalle.id_articulo.id_articulo)
                articulo = get_object_or_404(Articulo, pk=id_articulo)
                articulo.stock_actual = articulo.stock_actual + cantidad
                articulo.costo = detalle.costo_unitario
                articulo.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Borrado logico de una factura de compra"""
        instance = self.get_object()
        instance.estado = 'H'
        instance.save()
        detalle_factura_compra = DetalleFacturaCompra.objects.filter(facturacompra=instance.pk)
        for detalle in detalle_factura_compra:
            """Por cada articulo en detalle-factura-compra se actualiza el stock"""
            cantidad = int(detalle.cantidad)
            id_articulo = int(detalle.id_articulo.id_articulo)
            articulo = get_object_or_404(Articulo, pk=id_articulo)
            articulo.stock_actual = articulo.stock_actual - cantidad
            articulo.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetalleFacturaCompraView(viewsets.ModelViewSet):
    """ViewSet de detralle-factura-compra"""
    serializer_class = DetalleFacturaCompraModelSerializer
    queryset = DetalleFacturaCompra.objects.filter(estado='A')
    permission_classes = [IsAuthenticated]


class FacturaCompraSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """Buscador de facturas compras"""
    filter_backends = [SearchFilter]
    queryset = FacturaCompra.objects.filter()
    serializer_class = FacturaCompraModelSerializer
    search_fields = ['id_factura_compra',
                     'numero_factura',
                     'id_proveedor__propietario']
