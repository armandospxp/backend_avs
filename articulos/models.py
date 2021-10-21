from django.db import models
from utilidades.base_name import BaseModel


class Marca(BaseModel):
    id_marca = models.CharField(primary_key=True, max_length=64)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


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
    costo = models.DecimalField(decimal_places=2, max_digits=32)
    porc_iva = models.PositiveIntegerField()
    porc_comision = models.IntegerField()
    stock_actual = models.PositiveBigIntegerField()
    stock_minimo = models.IntegerField()
    ultima_compra = models.DateField()
    unidad_medida = models.CharField(max_length=20, choices=UNIDAD_MEDIDA_CHOICES)
    precio_unitario = models.DecimalField(decimal_places=4, max_digits=32)
    precio_mayorista = models.DecimalField(decimal_places=4, max_digits=32)
    precio_especial = models.DecimalField(decimal_places=4, max_digits=32)
