from django.db import models


class Configuracion(models.Model):
    id_impresora = models.AutoField(primary_key=True)
    nombre_impresora = models.CharField(null=False, max_length=50)
    numeracion_fija_factura = models.CharField(null=False, max_length=10)
    numero_factura = models.IntegerField(null=False)
    coordenada_x = models.CharField(max_length=10)
    coordenada_y = models.CharField(max_length=10)
