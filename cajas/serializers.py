# rest-framework
from rest_framework import serializers
# modelos de cajas
from cajas.models import ArqueoCaja, MovimientoCaja, RetiroDineroCaja


class ArqueoCajaModelSerializer(serializers.ModelSerializer):
    """Serializador de arqueo de cajas"""
    nombre_usuario = serializers.SerializerMethodField()

    class Meta:
        model = ArqueoCaja
        fields = '__all__'

    def get_nombre_usuario(self, obj):
        """Obtener el nombre de usuario"""
        return obj.id_empleado.first_name + ' ' + obj.id_empleado.last_name


class MovimientoCajaModelSerializer(serializers.ModelSerializer):
    """Serializador de movimiento de caja"""
    class Meta:
        model = MovimientoCaja
        fields = '__all__'


class RetiroDineroCajaModelSerializer(serializers.ModelSerializer):
    """Serializador de retiro de dinero de caja"""
    class Meta:
        model = RetiroDineroCaja
        fields = '__all__'
