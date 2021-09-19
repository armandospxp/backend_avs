from rest_framework import serializers

from configuracion.models import Configuracion


class ConfiguraionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = ['id_configuracion',
                  'nombre_empresa',
                  'comision_x_venta',
                  'estado_activo',
                  'ruc_empresa',
                  'direccion',
                  'telefono',
                  'pagina_web']
