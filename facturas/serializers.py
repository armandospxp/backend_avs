# drf-writable-nested
from drf_writable_nested import WritableNestedModelSerializer
# rest-framework
from rest_framework import serializers
# modelos de facturas
from facturas.models import DetalleFacturaCompra, FacturaCompra


class DetalleFacturaCompraModelSerializer(serializers.ModelSerializer):
    """Serializador de los detalles de la factura compra"""
    nombre_articulo = serializers.SerializerMethodField()
    codigo_articulo = serializers.SerializerMethodField()
    iva = serializers.SerializerMethodField()

    class Meta:
        model = DetalleFacturaCompra
        fields = '__all__'

    def get_nombre_articulo(self, obj):
        """Obtener el nombre del articulo"""
        return obj.id_articulo.nombre

    def get_codigo_articulo(self, obj):
        """Obtener el codigo de barras del articulo"""
        return obj.id_articulo.codigo_barras

    def get_iva(self, obj):
        """Obtener el iva del articulo"""
        return obj.id_articulo.porc_iva


class FacturaCompraModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """Serializador de Factura de Compras"""
    id_detalle_factura_compra = DetalleFacturaCompraModelSerializer(many=True)
    nombre_proveedor = serializers.SerializerMethodField()

    class Meta:
        model = FacturaCompra
        fields = '__all__'

    def get_nombre_proveedor(self, obj):
        """Obtener el nombre del proveedor"""
        return obj.id_proveedor.propietario

