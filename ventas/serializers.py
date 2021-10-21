from django.db import models
from django.db.models import fields
from rest_framework import serializers
from ventas.models import Venta, DetalleVenta
from personas.serializers import PersonaModelSerializers


class VentaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = ['id_venta', 'id_cliente', 'fecha', 'hora', 'total']


class DetalleVentaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'
