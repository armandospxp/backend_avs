from django.db import models


class Marca(models.Model):
    id_marca = models.CharField(primary_key=True, max_length=64)
    descripcion = models.CharField(max_length=100)


class Articulo(models.Model):
    KG = "Kiligramos"
    CJ = "Caja"
    UN = "Unidad"
    CC = "Centimetros Cubicos"
    UNIDAD_MEDIDA_CHOICES = [
        (KG, 'KILOGRAMOS'),
        (CJ, 'CAJA'),
        (UN, 'UNIDAD'),
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
