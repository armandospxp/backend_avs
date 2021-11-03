from django.db import models
from django.db.models import fields
from rest_framework import serializers
from ventas.models import Venta, DetalleVenta
from personas.serializers import PersonaModelSerializers


class DetalleVentaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class VentaModelSerializer(serializers.ModelSerializer):
    id_detalle_venta = DetalleVentaModelSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'
