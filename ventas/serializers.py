from rest_framework import serializers
from ventas.models import Venta, DetalleVenta
from drf_writable_nested import WritableNestedModelSerializer


class DetalleVentaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class VentaModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_venta = DetalleVentaModelSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id_venta',
                  'id_cliente',
                  'id_usuario',
                  'fecha',
                  'total',
                  'id_detalle_venta',
                  'tipo_factura'
                  ]
