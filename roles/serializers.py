from roles.models import Rol, Permiso, Modulo

from articulos import serializers


class PermisosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['descripcion']


class GroupModelSerializer(serializers.ModelSerializer):
    permissions = PermisosModelSerializer(read_only=True, many=True)

    class Meta:
        model = Rol
        fields = ['id', 'permissions']


class ModuloModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['*']
