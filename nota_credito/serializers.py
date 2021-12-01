from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from nota_credito.models import DetalleNotaCredito, NotaCreditoCliente
from utilidades.numero_letras import numero_a_letras


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
        if obj.id_articulo.porc_iva == 10:
            dato = int((int(obj.id_articulo.precio_unitario)*int(obj.cantidad))/11)
        else:
            dato = int((int(obj.id_articulo.precio_unitario) * int(obj.cantidad))/21)
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


class NotaCreditoVentaModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_nota_credito = DetalleNotaCreditoVentaModelSerializer(many=True)
    nombre_cliente = serializers.SerializerMethodField()
    nombre_usuario = serializers.SerializerMethodField()
    numero_factura = serializers.SerializerMethodField()
    monto_letras = serializers.SerializerMethodField()

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
        return str(obj.id_venta.id_usuario.configuracion.numeracion_fija_factura) + str(
            obj.id_venta.id_usuario.configuracion.numero_factura)

    def get_monto_letras(self, obj):
        return numero_a_letras(int(obj.monto_total))
