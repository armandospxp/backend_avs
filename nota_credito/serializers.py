from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from nota_credito.models import DetalleNotaCredito, NotaCreditoCliente
from utilidades.numero_letras import numero_a_letras


class DetalleNotaCreditoVentaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleNotaCredito
        fields = '__all__'


class NotaCreditoVentaModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_nota_credito = DetalleNotaCreditoVentaModelSerializer(many=True)

    class Meta:
        model = NotaCreditoCliente
        fields = '__all__'
