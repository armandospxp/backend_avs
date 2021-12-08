# django
from django.db import models
# modelo de articulos
from articulos.models import Articulo
# modelo de proveedores
from proveedores.models import Proveedor
# modelo base de utilidades
from utilidades.base_name import BaseModel


class Factura(BaseModel):
    """Modelo de facturas de compra"""
    CONTADO = 'CON'
    CREDITO = 'CRE'
    TIPO_FACTURA_CHOICES = [
        (CONTADO, 'Contado'),
        (CREDITO, 'Credito'),
    ]
    id_factura = models.AutoField(primary_key=True)
    fecha_vencimiento = models.DateField
    timbrado = models.IntegerField()
    numeracion_comienzo_factura = models.IntegerField
    cantidad_facturas = models.IntegerField()
    tipo_factura = models.CharField(max_length=3, choices=TIPO_FACTURA_CHOICES, default=CONTADO)


class DetalleFacturaCompra(BaseModel):
    """Modelo de detalle facturas de compra"""
    id_detalle_factura_compra = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    costo_unitario = models.PositiveIntegerField(default=0)
    subtotal = models.PositiveIntegerField(default=0)


class FacturaCompra(BaseModel):
    """Modelo de factura compra"""
    id_factura_compra = models.AutoField(primary_key=True)
    numero_factura = models.CharField(max_length=100)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    id_detalle_factura_compra = models.ManyToManyField(DetalleFacturaCompra)
    total_nota_credito = models.PositiveIntegerField(default=0)
