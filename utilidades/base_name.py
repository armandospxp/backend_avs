# python datetime
from datetime import date
# django
from django.db import models

# variable global de los tipos de estado
ESTADO_CHOICES = [('A', 'ACTIVO'),
                  ('H', 'HISTORICO')]


class BaseModel(models.Model):
    """Clase Base para los modelos, de los cuales van a heredar.
    Tienen 2 campos basicamente, el estado que puede ser Activo = 'A' o Historico = 'H' """
    class Meta:
        abstract = True
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    fecha_creacion = models.DateField(default=date.today)
