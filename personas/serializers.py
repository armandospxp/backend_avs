from rest_framework import serializers

from personas.models import Persona


class PersonaModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['id_persona', 'tipo_persona', 'nombre_apellido', 'propietario', 'direccion', 'telefono', 'ruc',
                  'cedula',
                  'correo_electronico',
                  'es_cliente',
                  'es_proveedor',
                  'fecha_nacimiento',
                  'estado_activo']
