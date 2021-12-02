from rest_framework import serializers

from utilidades.numero_letras import numero_a_letras
from ventas.models import Venta, DetalleVenta
from drf_writable_nested import WritableNestedModelSerializer


class DetalleVentaModelSerializer(serializers.ModelSerializer):
    sub_total_iva = serializers.SerializerMethodField()
    tipo_iva = serializers.SerializerMethodField()
    nombre_articulo = serializers.SerializerMethodField()
    precio_unitario = serializers.SerializerMethodField()
    codigo_articulo = serializers.SerializerMethodField()

    class Meta:
        model = DetalleVenta
        fields = '__all__'

    def get_sub_total_iva(self, obj):
        if obj.id_articulo.porc_iva == 10 and obj.cantidad < 3:
            dato = int((int(obj.id_articulo.precio_unitario) * int(obj.cantidad)) / 11)
        elif obj.id_articulo.porc_iva == 10 and 3 < obj.cantidad < 12:
            dato = int((int(obj.id_articulo.precio_mayorista) * int(obj.cantidad)) / 11)
        elif obj.id_articulo.porc_iva == 10 and obj.cantidad > 12:
            dato = int((int(obj.id_articulo.precio_especial) * int(obj.cantidad)) / 11)
        elif obj.id_articulo.porc_iva == 5 and obj.cantidad < 3:
            dato = int((int(obj.id_articulo.precio_unitario) * int(obj.cantidad)) / 21)
        elif obj.id_articulo.porc_iva == 5 and 3 < obj.cantidad < 12:
            dato = int((int(obj.id_articulo.precio_mayorista) * int(obj.cantidad)) / 21)
        else:
            dato = int((int(obj.id_articulo.precio_especial) * int(obj.cantidad)) / 21)
        return str(dato)

    def get_tipo_iva(self, obj):
        return str(obj.id_articulo.porc_iva)

    def get_nombre_articulo(self, obj):
        return obj.id_articulo.nombre

    def get_precio_unitario(self, obj):
        if obj.cantidad < 3:
            valor = obj.id_articulo.precio_unitario
        elif 3 < obj.cantidad < 12:
            valor = obj.id_articulo.precio_mayorista
        else:
            valor = obj.id_articulo.precio_especial
        return valor

    def get_codigo_articulo(self, obj):
        return obj.id_articulo.codigo_barras


class VentaModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_venta = DetalleVentaModelSerializer(many=True)
    nombre_cliente = serializers.SerializerMethodField()
    nombre_usuario = serializers.SerializerMethodField()
    numero_factura = serializers.SerializerMethodField()
    monto_letras = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['id_venta',
                  'id_cliente',
                  'id_usuario',
                  'fecha',
                  'total',
                  'id_detalle_venta',
                  'tipo_factura',
                  'numero_factura',
                  'nombre_cliente',
                  'nombre_usuario',
                  'monto_letras'
                  ]

    def get_nombre_cliente(self, obj):
        try:
            dato = obj.id_cliente.nombre_apellido
        except:
            dato = "SIN NOMBRE"
        return dato

    def get_nombre_usuario(self, obj):
        return obj.id_usuario.first_name + ' ' + obj.id_usuario.last_name

    def get_numero_factura(self, obj):
        return obj.numero_factura_asignado

    def get_monto_letras(self, obj):
        return numero_a_letras(int(obj.total))


class VentaListModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_venta = DetalleVentaModelSerializer(many=True)
    nombre_cliente = serializers.SerializerMethodField()
    nombre_usuario = serializers.SerializerMethodField()
    numero_factura = serializers.SerializerMethodField()
    monto_letras = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['id_venta',
                  'id_cliente',
                  'id_usuario',
                  'fecha',
                  'total',
                  'id_detalle_venta',
                  'tipo_factura',
                  'numero_factura',
                  'nombre_cliente',
                  'nombre_usuario',
                  'monto_letras'
                  ]

    def get_nombre_cliente(self, obj):
        try:
            dato = obj.id_cliente.nombre_apellido
        except:
            dato = "SIN NOMBRE"
        return dato

    def get_nombre_usuario(self, obj):
        return obj.id_usuario.first_name + ' ' + obj.id_usuario.last_name

    def get_numero_factura(self, obj):
        return str(obj.id_usuario.configuracion.numeracion_fija_factura) + str(
            obj.id_usuario.configuracion.numero_factura)

    def get_monto_letras(self, obj):
        return numero_a_letras(int(obj.total))


class DetalleVentaListModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
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
