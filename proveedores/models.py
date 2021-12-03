from typing import Tuple
from django.db import models

from utilidades.base_name import BaseModel


class Proveedor(BaseModel):
    FISICA = 'F'
    JURIDICA = 'J'
    VERDADERO = 'V'
    FALSO = 'F'
    TIPO_PERSONA_CHOICES = [
        (FISICA, 'Fisica'),
        (JURIDICA, 'Juridica'),
    ]
    VERDADER_FALSO_CHOICES = [
        (VERDADERO, 'Verdadero'),
        (FALSO, 'Falso'),
    ]
    id_proveedor = models.AutoField(primary_key=True)
    tipo_persona = models.CharField(max_length=1,
                                    choices=TIPO_PERSONA_CHOICES, default=FISICA, null=False, blank=False)
    propietario = models.CharField(null=False, blank=False, max_length=50)
    direccion = models.CharField(null=False, blank=False, max_length=100)
    telefono = models.CharField(null=False, blank=False, max_length=40)
    ruc = models.CharField(null=False, blank=False, max_length=50)
    correo_electronico = models.CharField(null=True, blank=True, max_length=50)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    estado_activo = models.CharField(max_length=1,
                                     choices=VERDADER_FALSO_CHOICES, default=VERDADERO)

    def __str__(self):
        return '{}'.format(self.propietario)


