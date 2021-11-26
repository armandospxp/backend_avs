from datetime import date

from django.db import models
from proveedores.models import Proveedor
from articulos.models import Articulo
from utilidades.base_name import BaseModel
from personas.models import Persona
from articulos.models import Articulo


class DetallePedido(BaseModel):
    id_detalle_pedido = models.BigAutoField(primary_key=True)
    id_articulo = models.ManyToManyField(Articulo)
    cantidad = models.PositiveIntegerField


class Pedido(BaseModel):
    id_pedido = models.BigAutoField(primary_key=True)
    id_cliente = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today())
    id_detalle_pedido = models.ForeignKey(DetallePedido)
