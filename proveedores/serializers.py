from rest_framework import serializers

from proveedores.models import Proveedor


class ProveedorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
