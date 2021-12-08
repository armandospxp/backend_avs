# rest-framework
from rest_framework import serializers
# modelos de articulos
from articulos.models import Articulo, Marca, AjusteStock


class ArticuloModelSerializer(serializers.ModelSerializer):
    """Serialzador de articulos"""
    class Meta:
        model = Articulo
        fields = ['id_articulo',
                  'id_marca',
                  'codigo_barras',
                  'nombre',
                  'costo',
                  'porc_iva',
                  'porc_comision',
                  'stock_actual',
                  'stock_minimo',
                  'ultima_compra',
                  'unidad_medida',
                  'precio_unitario',
                  'precio_mayorista',
                  'precio_especial',
                  ]


class MarcaModelSerializer(serializers.ModelSerializer):
    """Serializador de Marca"""
    class Meta:
        model = Marca
        fields = '__all__'


class ArticuloSearchModelSerializer(serializers.ModelSerializer):
    """Serializador para la busqueda de articulos"""
    id_marca = MarcaModelSerializer(read_only=True)

    class Meta:
        model = Articulo
        fields = ['id_articulo',
                  'id_marca',
                  'codigo_barras',
                  'nombre',
                  'costo',
                  'porc_iva',
                  'porc_comision',
                  'stock_actual',
                  'stock_minimo',
                  'ultima_compra',
                  'unidad_medida',
                  'precio_unitario',
                  'precio_mayorista',
                  'precio_especial',
                  ]


class ArticuloListSerializer(serializers.Serializer):
    """Serializador para lista de articulos"""
    id_articulo = serializers.IntegerField
    id_marca = MarcaModelSerializer(read_only=True)
    codigo_barras = serializers.CharField
    nombre = serializers.CharField
    costo = serializers.IntegerField
    porc_iva = serializers.IntegerField
    porc_comision = serializers.IntegerField
    stock_actual = serializers.IntegerField
    stock_minimo = serializers.IntegerField
    ultima_compra = serializers.DateField
    unidad_medida = serializers.CharField
    precio_unitario = serializers.IntegerField
    precio_mayorista = serializers.IntegerField
    precio_especial = serializers.IntegerField


class AjusteStockModelSerializer(serializers.ModelSerializer):
    """Serializador para ajuste de articulos"""
    class Meta:
        model = AjusteStock
        fields = '__all__'
