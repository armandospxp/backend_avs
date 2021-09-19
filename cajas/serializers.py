from rest_framework import serializers

from cajas.models import Caja


class CajaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = ['id_caja', 'id_empleado', 'descripcion', 'activo']
