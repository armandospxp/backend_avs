from django.db import models

from utilidades.base_name import BaseModel


class Factura(BaseModel):
    CONTADO = 'CON'
    CREDITO = 'CRE'
    TIPO_FACTURA_CHOICES = [
        (CONTADO, 'Contado'),
        (CREDITO, 'Credito'),
    ]
    id_factura = models.AutoField(primary_key=True)
    fecha_vencimiento = models.DateField
    timbrado = models.IntegerField(max_length=10)
    numeracion_comienzo_factura = models.IntegerField
    cantidad_facturas = models.IntegerField(max_length=3)
    tipo_factura = models.CharField(max_length=3, choices=TIPO_FACTURA_CHOICES, default=CONTADO)
