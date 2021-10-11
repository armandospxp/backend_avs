from django.db import models
from datetime import date, datetime
from django.db.models.base import Model
from articulos.models import Articulo
from personas.models import Persona

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today())
    hora = models.TimeField(default=datetime.now().strftime("%H:%M:%S"))

class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(max_length=3)
    sub_total = models.IntegerField
    precio_total = models.IntegerField

