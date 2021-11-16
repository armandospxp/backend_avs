from rest_framework import serializers
from compras.models import OrdenCompra


class OrdenCompraModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenCompra
        fields = '__all__'
