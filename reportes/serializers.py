# rest-framework
from rest_framework import serializers


class ReporteArticulosVendidos(serializers.Serializer):
    """Serialzier de reporte de articulos vendidos"""
    id_articulo__nombre = serializers.CharField()
    sub_total = serializers.IntegerField()
    total = serializers.IntegerField()
    cantidad_vendida = serializers.IntegerField()


class ReporteTopVendendores(serializers.Serializer):
    """Serializer de Top 5 Vendedores"""
    nombre_apellido = serializers.SerializerMethodField()
    id_usuario__first_name = serializers.CharField()
    id_usuario__last_name = serializers.CharField()
    cantidad_vendida = serializers.IntegerField()

    def get_nombre_apellido(self, obj):
        """Obtiene el nombre y apellido del Vendedor"""
        return obj['id_usuario__first_name']+' '+obj['id_usuario__last_name']


class ReporteListaArticulosStock(serializers.Serializer):
    """Serializador de Reporte de Stock de Articulos"""
    id_articulo = serializers.IntegerField()
    codigo_barras = serializers.CharField()
    stock_minimo = serializers.IntegerField()
    stock_actual = serializers.IntegerField()
