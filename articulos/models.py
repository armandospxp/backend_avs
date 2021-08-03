from django.db import models


class Articulo(models.Model):
    """Modelo de articulos """
    id_articulo = models.IntegerField(primary_key=True)
    codigo = models.ForeignKey(Marca, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=80, blank=False, null=False)
    costo = models.DecimalField(decimal_places=2)
    porc_iva = models.PositiveIntegerField()
    porc_comision = models.IntegerField()
    stock_actual = models.PositiveBigIntegerField()
    stock_minimo = models.IntegerField()
    ultima_compra = models.DateField()
    unidad_medida = models.CharField(max_length=4)
    precio_unitario = models.DecimalField(decimal_places=4)
    precio_mayorista = models.DecimalField(decimal_places=4)
    precio_especial = models.DecimalField(decimal_places=4)


class Marca(models.Model):
    codigo = models.CharField(primary_key=True)
    descripcion = models.CharField(max_length=100)
