from rest_framework import serializers

from articulos.models import Articulo, Marca


class ArticuloModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ['id_articulo', 'codigo', 'nombre', 'costo', 'porc_iva', 'porc_comision', 'stock_actual', 'stock_minimo', 'ultima_compra',
                  'unidad_medida', 'precio_unitario', 'precio_mayorista', 'precio_especial']


class MarcaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'
