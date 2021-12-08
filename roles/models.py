# django
from django.db import models
# modelo de usuarios
from users.models import User


class Modulo(models.Model):
    """Modelo de modulo"""
    id_modulo = models.AutoField(primary_key=True)
    nombre_modulo = models.CharField(max_length=30)


class Permiso(models.Model):
    """Modelo de permiso"""
    id_permiso = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15)


class Rol(models.Model):
    """Modelo de rol"""
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    usuario = models.ManyToManyField(User)
    permiso = models.ManyToManyField(Permiso)
    modulo = models.ManyToManyField(Modulo)
