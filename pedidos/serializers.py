from rest_framework import serializers
from pedidos.models import Pedido, DetallePedido
from drf_writable_nested import WritableNestedModelSerializer


class DetallePedidoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'


class PedidoModelSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    id_detalle_pedido = DetallePedidoModelSerializer(many=True)

    class Meta:
        model = Pedido
        fields = '__all__'
