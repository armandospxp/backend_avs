from rest_framework import serializers


class ReporteArticulosVendidos(serializers.Serializer):
    id_articulo__nombre = serializers.CharField()
    sub_total = serializers.IntegerField()
    total = serializers.IntegerField()
    cantidad_vendida = serializers.IntegerField()
