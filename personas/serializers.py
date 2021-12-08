# rest-framework
from rest_framework import serializers
# modelo de personas
from personas.models import Persona


class PersonaModelSerializers(serializers.ModelSerializer):
    """Serializador de Personas"""
    class Meta:
        model = Persona
        fields = ['id_persona', 'tipo_persona', 'nombre_apellido', 'propietario', 'direccion', 'telefono', 'ruc',
                  'cedula',
                  'correo_electronico',
                  'es_cliente',
                  'es_proveedor',
                  'fecha_nacimiento',
                  'estado_activo']


class PersonaListSerializer(serializers.Serializer):
    """Serializador de Lista de Personas"""
    id_persona = serializers.IntegerField
    tipo_persona = serializers.CharField
    nombre_apellido = serializers.CharField
    propietario = serializers.CharField
    direccion = serializers.CharField
    telefono = serializers.CharField
    ruc = serializers.CharField
    cedula = serializers.CharField
    correo_electronico = serializers.CharField
    es_cliente = serializers.CharField
    fecha_nacimiento = serializers.DateField
    estado_activo = serializers.CharField
