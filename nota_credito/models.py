from datetime import date

from django.db import models

from articulos.models import Articulo
from utilidades.base_name import BaseModel
from ventas.models import Venta


class DetalleNotaCredito(BaseModel):
    id_detalle_nota_credito = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)


class NotaCreditoCliente(BaseModel):
    id_nota_credito_cliente = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_detalle_nota_credito = models.ManyToManyField(DetalleNotaCredito, blank=False)
    fecha = models.DateField(default=date.today)
    monto_total = models.PositiveIntegerField(default=0)
