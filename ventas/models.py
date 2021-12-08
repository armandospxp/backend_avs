# django
from django.db import models
# python
from datetime import date, datetime
# modelo de articulos
from articulos.models import Articulo
# modelo de personas
from personas.models import Persona
# modelo de usuarios
from users.models import User
# modelo base de utilidades
from utilidades.base_name import BaseModel


class DetalleVenta(BaseModel):
    """Modeo de Detalle Ventas"""
    id_detalle_venta = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False, null=False, default=1)
    sub_total = models.IntegerField(blank=False, null=False, default=0)


class Venta(BaseModel):
    """Modelo de Ventas"""
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
    hora = models.TimeField(default=datetime.now().time().strftime("%H:%M:%S"))
    total = models.PositiveIntegerField(blank=False, null=False, default=0)
    id_detalle_venta = models.ManyToManyField(DetalleVenta, blank=False)
    tipo_factura = models.CharField(max_length=3, choices=TIPO_FACTURA_CHOICES, default="CON")
    numero_factura_asignado = models.CharField(blank=True, null=True, max_length=30)
    total_nota_credito = models.PositiveIntegerField(default=0)
