from django.db import models

from users.models import User


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=30)
    usuario = models.ManyToManyField(User)
    permiso = models.ManyToManyField(Permiso)
    modulo = models.ManyToManyField(Modulo)


class Modulo(models.Model):
    id_modulo = models.AutoField(primary_key=True)
    nombre_modulo = models.CharField(max_length=30)


class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15)
