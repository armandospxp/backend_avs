import pdb

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from nota_credito.models import DetalleNotaCredito, NotaCreditoCliente, NotaCreditoProveedor, \
    DetalleNotaCreditoProveedor
from utilidades.numero_letras import numero_a_letras
from ventas.models import Venta, DetalleVenta

AUX_ID_VENTA = None
AUX_ID_DETALLE_VENTA = None
AUX_CANTIDAD = ""


class DetalleNotaCreditoVentaModelSerializer(serializers.ModelSerializer):
    sub_total_iva = serializers.SerializerMethodField()
    tipo_iva = serializers.SerializerMethodField()
    nombre_articulo = serializers.SerializerMethodField()
    precio_unitario = serializers.SerializerMethodField()
    codigo_articulo = serializers.SerializerMethodField()

    class Meta:
        model = DetalleNotaCredito
        fields = '__all__'

    def get_sub_total_iva(self, obj):
        AUX_ID_VENTA = obj.id_venta.id_venta
        detalle_venta = get_object_or_404(DetalleVenta.objects.filter(venta=AUX_ID_VENTA))
        AUX_CANTIDAD = int(detalle_venta.cantidad)
        if obj.id_articulo.porc_iva == 10 and AUX_CANTIDAD < 3:
            dato = int((int(obj.id_articulo.precio_unitario) * int(obj.cantidad)) / 11)
        elif obj.id_articulo.porc_iva == 10 and 3 < AUX_CANTIDAD < 12:
            dato = int((int(obj.id_articulo.precio_mayorista) * int(obj.cantidad)) / 11)
        elif obj.id_articulo.porc_iva == 10 and AUX_CANTIDAD > 12:
            dato = int((int(obj.id_articulo.precio_unitario) * int(obj.cantidad)) / 11)
        elif obj.id_articulo.porc_iva == 5 and AUX_CANTIDAD < 3:
            dato = int((int(obj.id_articulo.precio_mayorista) * int(obj.cantidad)) / 21)
        elif obj.id_articulo.porc_iva == 5 and 3 < AUX_CANTIDAD < 12:
            dato = int((int(obj.id_articulo.precio_mayorista) * int(obj.cantidad)) / 21)
        else:
            dato = int((int(obj.id_articulo.precio_especial) * int(obj.cantidad)) / 21)
        return str(dato)

    def get_tipo_iva(self, obj):
        return str(obj.id_articulo.porc_iva)

    def get_nombre_articulo(self, obj):
        return obj.id_articulo.nombre

    def get_precio_unitario(self, obj):
        AUX_ID_VENTA = obj.id_venta.id_venta
        detalle_venta = get_object_or_404(DetalleVenta.objects.filter(venta=AUX_ID_VENTA))
        AUX_CANTIDAD = int(detalle_venta.cantidad)
        # pdb.set_trace()
        if AUX_CANTIDAD < 3:
            valor = obj.id_articulo.precio_unitario
        elif 3 < AUX_CANTIDAD < 12:
            valor = obj.id_articulo.precio_mayorista
        else:
            valor = obj.id_articulo.precio_especial
        return valor

    def get_codigo_articulo(self, obj):
        return obj.id_articulo.codigo_barras


class NotaCreditoVentaModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_nota_credito = DetalleNotaCreditoVentaModelSerializer(many=True)
    nombre_cliente = serializers.SerializerMethodField()
    nombre_usuario = serializers.SerializerMethodField()
    numero_factura = serializers.SerializerMethodField()
    monto_letras = serializers.SerializerMethodField()
    id_cliente = serializers.SerializerMethodField()

    class Meta:
        model = NotaCreditoCliente
        fields = '__all__'

    def get_nombre_cliente(self, obj):
        try:
            dato = obj.id_venta.id_cliente.nombre_apellido
        except:
            dato = "SIN NOMBRE"
        return dato

    def get_nombre_usuario(self, obj):
        return obj.id_venta.id_usuario.first_name + ' ' + obj.id_venta.id_usuario.last_name

    def get_numero_factura(self, obj):
        return obj.id_venta.numero_factura_asignado

    def get_monto_letras(self, obj):
        return numero_a_letras(int(obj.monto_total))

    def get_id_cliente(self, obj):
        return obj.id_venta.id_cliente.pk


class DetalleNotaCreditoProveedorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleNotaCreditoProveedor
        fields = '__all__'


class NotaCreditoProveedorModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_nota_credito_proveedor = DetalleNotaCreditoProveedorModelSerializer(many=True)

    class Meta:
        model = NotaCreditoProveedor
        fields = '__all__'
