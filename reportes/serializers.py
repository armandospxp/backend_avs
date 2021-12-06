import pdb

from rest_framework import serializers


class ReporteArticulosVendidos(serializers.Serializer):
    id_articulo__nombre = serializers.CharField()
    sub_total = serializers.IntegerField()
    total = serializers.IntegerField()
    cantidad_vendida = serializers.IntegerField()


class ReporteTopVendendores(serializers.Serializer):
    nombre_apellido = serializers.SerializerMethodField()
    id_usuario__first_name = serializers.CharField()
    id_usuario__last_name = serializers.CharField()
    cantidad_vendida = serializers.IntegerField()

    def get_nombre_apellido(self, obj):
        return obj['id_usuario__first_name']+' '+obj['id_usuario__last_name']
