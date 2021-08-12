from rest_framework import serializers

from articulos.models import Articulo, Marca


class ArticuloModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo


class MarcaModelSerializer(serializers.Serializer):
    class Meta:
        model = Marca
