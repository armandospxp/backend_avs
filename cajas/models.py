from django.db import models

class Caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    id_empleado = models.Fo