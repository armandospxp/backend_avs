from rest_framework import serializers

from proveedores.models import Proveedor


class ProveedorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id_proveedor',
                  'tipo_persona',
                  'nombre',
                  'apellido',
                  'propietario',
                  'direccion',
                  'telefono',
                  'ruc',
                  'correo_electronico',
                  'fecha_nacimiento',
                  'estado_activo']
