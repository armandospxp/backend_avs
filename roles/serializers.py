from rest_framework import serializers

from roles.models import Rol
from roles.models import Permiso
from roles.models import Modulo


class PermisosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['descripcion']


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class ModuloModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id_modulo', 'nombre_modulo', 'permisomodulorol']
