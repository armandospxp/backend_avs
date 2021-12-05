from django.db import models

from users.models import User
from utilidades.base_name import BaseModel


class Marca(BaseModel):
    id_marca = models.CharField(primary_key=True, max_length=64)
    descripcion = models.CharField(max_length=100)


class Articulo(BaseModel):
    KILOGRAMOS = "KG"
    CAJA = "CJ"
    UNIDAD = "UN"
    CC = "CC"
    UNIDAD_MEDIDA_CHOICES = [
        (KILOGRAMOS, 'KILOGRAMOS'),
        (CAJA, 'CAJA'),
        (UNIDAD, 'UNIDAD'),
        (CC, 'CENTIMETROS CÚBICOS')
    ]
    """Modelo de articulos """
    id_articulo = models.BigAutoField(primary_key=True)
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=15, blank=False, null=False)
    nombre = models.CharField(max_length=80, blank=False, null=False)
    costo = models.IntegerField()
    porc_iva = models.PositiveIntegerField()
    porc_comision = models.IntegerField()
    stock_actual = models.PositiveBigIntegerField()
    stock_minimo = models.IntegerField()
    ultima_compra = models.DateField()
    unidad_medida = models.CharField(max_length=20, choices=UNIDAD_MEDIDA_CHOICES)
    precio_unitario = models.IntegerField()
    precio_mayorista = models.IntegerField()
    precio_especial = models.IntegerField()

    def __str__(self):
        return self.nombre


class AjusteStock(BaseModel):
    ALTA = "A"
    BAJA = "B"
    TIPO_AJUSTE_CHOICES = [
        (ALTA, 'ALTA'),
        (BAJA, 'BAJA')
    ]
    id_ajuste_stock = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    tipo_ajuste = models.CharField(max_length=1, choices=TIPO_AJUSTE_CHOICES)
    id_usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    cantidad = models.PositiveIntegerField(default=0)
    motivo_ajuste = models.CharField(max_length=200)
