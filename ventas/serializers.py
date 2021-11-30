import pdb

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


class VentaListModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_venta = DetalleVentaModelSerializer(many=True)
    nombre_cliente = serializers.SerializerMethodField()
    nombre_usuario = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['id_venta',
                  'id_cliente',
                  'id_usuario',
                  'fecha',
                  'total',
                  'id_detalle_venta',
                  'tipo_factura',
                  'nombre_cliente',
                  'nombre_usuario'
                  ]

    def get_nombre_cliente(self, obj):
        try:
            dato = obj.id_cliente.nombre_apellido
        except:
            dato = "SIN NOMBRE"
        return dato

    def get_nombre_usuario(self, obj):
        return obj.id_usuario.first_name+' '+obj.id_usuario.last_name