from rest_framework import serializers

from configuracion.models import Configuracion


class ConfiguraionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'
