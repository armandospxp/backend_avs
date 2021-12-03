from rest_framework import serializers

from cajas.models import ArqueoCaja, MovimientoCaja, RetiroDineroCaja


class ArqueoCajaModelSerializer(serializers.ModelSerializer):
    nombre_usuario = serializers.SerializerMethodField()

    class Meta:
        model = ArqueoCaja
        fields = '__all__'

    def get_nombre_usuario(self, obj):
        return obj.id_empleado.first_name + ' ' + obj.id_empleado.last_name


class MovimientoCajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCaja
        fields = '__all__'


class RetiroDineroCajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetiroDineroCaja
        fields = '__all__'
