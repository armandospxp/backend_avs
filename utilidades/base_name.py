from django.db import models
from django import utils

ESTADO_CHOICES = [('A', 'ACTIVO'),
                  ('H', 'HISTORICO')]


class BaseModel(models.Model):
    class Meta:
        abstract = True
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    fecha_creacion = models.DateField(default=utils.timezone.now)
