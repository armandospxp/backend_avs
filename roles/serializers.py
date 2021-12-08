# rest-framework
from rest_framework import serializers

# modelo de roles
from roles.models import Rol
from roles.models import Permiso
from roles.models import Modulo
# serializers de roles
from users.serializers import UserModelSerializer


class PermisosModelSerializer(serializers.ModelSerializer):
    """Serialziador de permisos"""
    class Meta:
        model = Permiso
        fields = '__all__'


class ModuloModelSerializer(serializers.ModelSerializer):
    """Serialziador de modulos"""
    class Meta:
        model = Modulo
        fields = '__all__'


class RolModelSerializer(serializers.ModelSerializer):
    """Serializador de roles"""
    usuario = UserModelSerializer(read_only=True, many=True)

    class Meta:
        model = Rol
        fields = '__all__'
