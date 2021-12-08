# drf_writable_nested
from drf_writable_nested import WritableNestedModelSerializer
# rest_framework
from rest_framework import serializers

# modelo de notas
from nota_credito.models import DetalleNotaCredito, NotaCreditoCliente, NotaCreditoProveedor, \
    DetalleNotaCreditoProveedor
# Modelo de ventas
from ventas.models import Venta, DetalleVenta

# libreria numero_letras de utilidades
from utilidades.numero_letras import numero_a_letras

# variables globales auxiliares
AUX_ID_VENTA = None
AUX_ID_DETALLE_VENTA = None
AUX_CANTIDAD = ""


class DetalleNotaCreditoVentaModelSerializer(serializers.ModelSerializer):
    """Serialziador para los detalles de nota de credito venta"""
    sub_total_iva = serializers.SerializerMethodField()
    tipo_iva = serializers.SerializerMethodField()
    nombre_articulo = serializers.SerializerMethodField()
    precio_unitario = serializers.SerializerMethodField()
    codigo_articulo = serializers.SerializerMethodField()

    class Meta:
        model = DetalleNotaCredito
        fields = '__all__'

    def get_sub_total_iva(self, obj):
        """Funcion para calcular el subtotal iva de cada articulo"""
        AUX_ID_VENTA = obj.id_venta.id_venta
        detalle_venta = DetalleVenta.objects.filter(venta=AUX_ID_VENTA).filter(id_articulo=obj.id_articulo)
        global AUX_CANTIDAD
        for d in detalle_venta:
            AUX_CANTIDAD = d.cantidad
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
        """Obtener el tipo iva de un articulo"""
        return str(obj.id_articulo.porc_iva)

    def get_nombre_articulo(self, obj):
        """Obtener el nombre de un articulo"""
        return obj.id_articulo.nombre

    def get_precio_unitario(self, obj):
        """Obtener el precio unitario de cada articulo"""
        AUX_ID_VENTA = obj.id_venta.id_venta
        detalle_venta = DetalleVenta.objects.filter(venta=AUX_ID_VENTA).filter(id_articulo=obj.id_articulo)
        global AUX_CANTIDAD
        for d in detalle_venta:
            AUX_CANTIDAD = d.cantidad
        if AUX_CANTIDAD < 3:
            valor = obj.id_articulo.precio_unitario
        elif 3 < AUX_CANTIDAD < 12:
            valor = obj.id_articulo.precio_mayorista
        else:
            valor = obj.id_articulo.precio_especial
        return valor

    def get_codigo_articulo(self, obj):
        """Obtener el codigo de barras de un articulo"""
        return obj.id_articulo.codigo_barras


class NotaCreditoVentaModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """Serializador de Nota credito venta"""
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
        """Obtener el nombre del cliente"""
        try:
            dato = obj.id_venta.id_cliente.nombre_apellido
        except:
            dato = "SIN NOMBRE"
        return dato

    def get_nombre_usuario(self, obj):
        """Obtener el nombre del empleado que ha sido parte de la venta"""
        return obj.id_venta.id_usuario.first_name + ' ' + obj.id_venta.id_usuario.last_name

    def get_numero_factura(self, obj):
        """Obtener el numero de factura de la venta"""
        return obj.id_venta.numero_factura_asignado

    def get_monto_letras(self, obj):
        """Obtener el monto en letras para la factura"""
        return numero_a_letras(int(obj.monto_total))

    def get_id_cliente(self, obj):
        """Obtener el id del cliente"""
        return obj.id_venta.id_cliente.pk


class DetalleNotaCreditoProveedorModelSerializer(serializers.ModelSerializer):
    """Serializador de detalle nota credito proveedor"""
    codigo_articulo = serializers.SerializerMethodField()
    nombre_articulo = serializers.SerializerMethodField()

    class Meta:
        model = DetalleNotaCreditoProveedor
        fields = '__all__'

    def get_codigo_articulo(self, obj):
        """Obtener el codigo del articulo"""
        return obj.id_articulo.codigo_barras

    def get_nombre_articulo(self, obj):
        """Obtener el nombre del articulo"""
        return obj.id_articulo.nombre


class NotaCreditoProveedorModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    """Serializador para la nota credito de proveedor"""
    id_detalle_nota_credito_proveedor = DetalleNotaCreditoProveedorModelSerializer(many=True)
    nombre_proveedor = serializers.SerializerMethodField()
    numero_factura = serializers.SerializerMethodField()

    class Meta:
        model = NotaCreditoProveedor
        fields = '__all__'

    def get_nombre_proveedor(self, obj):
        """Obtner el nombre del proveedor"""
        return obj.id_factura_compra.id_proveedor.propietario

    def get_numero_factura(self, obj):
        """Obtener el numero de factura"""
        return obj.id_factura_compra.numero_factura
