from django.db import models
from datetime import date, datetime
from django.db.models.base import Model
from articulos.models import Articulo
from personas.models import Persona
from django.utils import timezone
from django import utils


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Persona, null=False, blank=False, on_delete=models.CASCADE)
    fecha = models.DateField(default=utils.timezone.now)
    hora = models.TimeField(default=timezone.now().strftime("%H:%M:%S"))
    total = models.IntegerField(blank=False, null=False, default=0)


class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    sub_total = models.IntegerField(blank=False, null=False, default=0)
