from django.db import models


class Persona(models.Model):
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
    nombre_apellido = models.CharField(blank=False, null=False)
    propietario = models.CharField(null=True, blank=True)
    direccion = models.CharField(null=False, blank=False)
    telefono = models.CharField(null=False, blank=False)
    ruc = models.CharField(null=True, blank=True)
    cedula = models.CharField(null=True, blank=True)
    correo_electronico = models.CharField(null=True, blank=True)
    es_cliente = models.CharField(max_length=1,
                                  choices=VERDADER_FALSO_CHOICES, default=VERDADERO)
    es_proveedor = models.CharField(max_length=1,
                                    choices=VERDADER_FALSO_CHOICES, default=FALSO)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    estado_activo = models.CharField(max_length=1,
                                     choices=VERDADER_FALSO_CHOICES, default=VERDADERO)
