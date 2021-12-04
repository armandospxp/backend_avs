import pdb

from django.shortcuts import get_object_or_404
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from articulos.models import Articulo
from facturas.models import DetalleFacturaCompra, FacturaCompra


class DetalleFacturaCompraModelSerializer(serializers.ModelSerializer):
    nombre_articulo = serializers.SerializerMethodField()
    codigo_articulo = serializers.SerializerMethodField()
    iva = serializers.SerializerMethodField()

    class Meta:
        model = DetalleFacturaCompra
        fields = '__all__'

    def get_nombre_articulo(self, obj):
        return obj.id_articulo.nombre

    def get_codigo_articulo(self, obj):
        return obj.id_articulo.codigo_barras

    def get_iva(self, obj):
        return obj.id_articulo.porc_iva


class FacturaCompraModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_factura_compra = DetalleFacturaCompraModelSerializer(many=True)
    nombre_proveedor = serializers.SerializerMethodField()

    class Meta:
        model = FacturaCompra
        fields = '__all__'

    def get_nombre_proveedor(self, obj):
        return obj.id_proveedor.propietario

