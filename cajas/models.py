from datetime import date, datetime

from django.db import models

from personas.models import Persona
from users.models import User


class ArqueoCaja(models.Model):
    id_arqueo_caja = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(User, on_delete=models.CASCADE)
    monto_apertura = models.PositiveIntegerField(null=False, blank=False, default=0)
    monto_cierre = models.PositiveIntegerField(null=False, blank=False, default=0)
    monto_calculado = models.IntegerField(default=0)
    fecha_apertura = models.DateField(null=False, blank=False, default=date.today)
    fecha_cierre = models.DateField(null=True, blank=True)
    hora_cierre = models.TimeField(null=True, blank=True)
    monto_comprobante = models.PositiveIntegerField(default=0)
    descripcion_comprobante = models.CharField(null=True, max_length=100)


class MovimientoCaja(models.Model):
    VENTA = "V"
    RETIRO = "R"
    TIPO_FACTURA_CHOICES = [
        (VENTA, 'V'),
        (RETIRO, 'R'),
    ]
    id_movimiento_caja = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(blank=False, null=False, max_length=1, choices=TIPO_FACTURA_CHOICES)
    monto = models.BigIntegerField(blank=False, null=False, default=0)
    fecha = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now().time().strftime("%H:%M:%S"))
