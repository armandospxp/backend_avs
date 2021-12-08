# django
from django.db import models
# Modelo base de utilidades
from utilidades.base_name import BaseModel


class Persona(BaseModel):
    """Modelo de Personas"""
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
    id_persona = models.AutoField(primary_key=True)
    tipo_persona = models.CharField(max_length=1,
                                    choices=TIPO_PERSONA_CHOICES, default=FISICA)
    nombre_apellido = models.CharField(blank=False, null=False, max_length=100)
    propietario = models.CharField(null=True, blank=True, max_length=50)
    direccion = models.CharField(null=False, blank=False, max_length=100)
    telefono = models.CharField(null=False, blank=False, max_length=40)
    ruc = models.CharField(null=True, blank=True, max_length=50)
    cedula = models.CharField(null=True, blank=True, max_length=50)
    correo_electronico = models.CharField(null=True, blank=True, max_length=50)
    es_cliente = models.CharField(max_length=1,
                                  choices=VERDADER_FALSO_CHOICES, default=VERDADERO)
    es_proveedor = models.CharField(max_length=1,
                                    choices=VERDADER_FALSO_CHOICES, default=FALSO)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    estado_activo = models.CharField(max_length=1,
                                     choices=VERDADER_FALSO_CHOICES, default=VERDADERO)

    def __str__(self):
        return '{}'.format(self.nombre_apellido)
