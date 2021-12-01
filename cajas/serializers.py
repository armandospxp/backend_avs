from rest_framework import serializers

from cajas.models import Caja, ArqueoCaja, MovimientoCaja


class CajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'


class ArqueoCajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArqueoCaja
        fields = '__all__'


class MovimientoCajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCaja
        fields = '__all__'
