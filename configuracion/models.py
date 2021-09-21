from django.db import models


class Configuracion(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(null=False, max_length=50)
    comision_x_venta = models.IntegerField(null=False)
    estado_activo = models.BooleanField(default=True)
    ruc_empresa = models.CharField(max_length=40)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    pagina_web = models.CharField(null=True, blank=True, max_length=100)
