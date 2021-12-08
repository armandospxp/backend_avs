# rest-framework
from rest_framework import serializers
# modelo de configuracion
from configuracion.models import Configuracion


class ConfiguraionModelSerializer(serializers.ModelSerializer):
    """Serializador de Configruacion"""
    class Meta:
        model = Configuracion
        fields = '__all__'
