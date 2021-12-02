from rest_framework import serializers

from cajas.models import ArqueoCaja, MovimientoCaja


class ArqueoCajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArqueoCaja
        fields = '__all__'


class MovimientoCajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCaja
        fields = '__all__'
