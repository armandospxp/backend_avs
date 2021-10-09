from rest_framework import serializers

from roles.models import Rol
from roles.models import Permiso
from roles.models import Modulo
from users.serializers import UserModelSerializer


class PermisosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'


class ModuloModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'


class RolModelSerializer(serializers.ModelSerializer):
    usuario = UserModelSerializer(read_only=True, many=True)
    # permiso = PermisosModelSerializer(read_only=True, many=True)
    # modulo = ModuloModelSerializer(read_only=True, many=True)

    class Meta:
        model = Rol
        fields = '__all__'
        depth = 1
