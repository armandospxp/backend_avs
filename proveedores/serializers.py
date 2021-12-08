# rest-framework
from rest_framework import serializers
# modelo de proveedor
from proveedores.models import Proveedor


class ProveedorModelSerializer(serializers.ModelSerializer):
    """Serializador de Proveedores"""
    class Meta:
        model = Proveedor
        fields = '__all__'
