from datetime import date

from django.db import models
from proveedores.models import Proveedor
from articulos.models import Articulo


class OrdenCompra(models.Model):
    IVA10 = 10
    IVA5 = 5
    IVA_CHOICES = [
        (IVA10, 'IVA 10%'),
        (IVA5, 'IVA 5%'),
    ]
    id_orden_compra = models.BigAutoField(primary_key=True)
    fecha_entrada = models.DateField(default=date.today)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    precio = models.IntegerField(blank=False, null=False)
    iva = models.IntegerField(choices=IVA_CHOICES)
    sub_total = models.IntegerField(blank=False, null=False, default=0)
