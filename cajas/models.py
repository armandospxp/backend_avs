from django.db import models

from personas.models import Persona


class Caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Persona, on_delete=models.CASCADE)
    descripcion = models.CharField(null=False, blank=False)
    activo = models.BooleanField(default=True)


class ArqueoCaja(models.Model):
    id_arqueo_caja = models.AutoField(primary_key=True)
    id_caja = models.ForeignKey(Caja)
    id_empleado = models.ForeignKey(Persona)
    monto_apertura = models.BigIntegerField(null=False, blank=False)
    monto_cierre = models.BigIntegerField(null=False, blank=False)
    fecha_apertura = models.DateField(null=False, blank=False)
    fecha_cierre = models.DateField(null=False, blank=False)
    hora_cierre = models.TimeField(null=False, blank=False)


class MovimientoCaja(models.Model):
    id_movimiento_caja = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Persona)
    tipo_movimiento = models.CharField(blank=False, null=False)
    monto = models.BigIntegerField(blank=False, null=False)


class ComprobanteMovimiento(models.Model):
    id_comprobante_movimiento = models.AutoField(primary_key=True)
    id_movimiento_caja = models.ForeignKey(MovimientoCaja)
    tipo_comprobante = models.CharField(null=False, blank=False)
