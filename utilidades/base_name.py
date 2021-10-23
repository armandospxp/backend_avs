from datetime import date

from django.db import models

ESTADO_CHOICES = [('A', 'ACTIVO'),
                  ('H', 'HISTORICO')]


class BaseModel(models.Model):
    class Meta:
        abstract = True
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    fecha_creacion = models.DateField(default=date.today)
