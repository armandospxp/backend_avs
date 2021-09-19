from rest_framework import serializers

from roles.models import Rol
from roles.models import Permiso
from roles.models import Modulo


class PermisosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['descripcion']


class GroupModelSerializer(serializers.ModelSerializer):
    permissions = PermisosModelSerializer(read_only=True, many=True)

    class Meta:
        model = Rol
        fields = ['id_rol', 'permissions']


class ModuloModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['*']
