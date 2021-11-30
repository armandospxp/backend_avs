from django.db import models
from datetime import date, datetime
from django.db.models.base import Model
from articulos.models import Articulo
from personas.models import Persona
from django.utils import timezone
from django import utils

from users.models import User
from utilidades.base_name import BaseModel


class DetalleVenta(BaseModel):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    sub_total = models.IntegerField(blank=False, null=False, default=0)


class Venta(BaseModel):
    CONTADO = "CON"
    CREDITO = "CRE"
    TIPO_FACTURA_CHOICES = [
        (CONTADO, 'CONTADO'),
        (CREDITO, 'CREDITO'),
    ]
    id_venta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(User, default=13, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Persona, null=False, blank=False, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    hora = models.TimeField
    total = models.IntegerField(blank=False, null=False, default=0)
    id_detalle_venta = models.ManyToManyField(DetalleVenta, blank=False)
    tipo_factura = models.CharField(max_length=3, choices=TIPO_FACTURA_CHOICES, default="CON")
