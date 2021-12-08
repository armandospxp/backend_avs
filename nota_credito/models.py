# python datetime
from datetime import date
# django
from django.db import models
# modelo de articulos
from articulos.models import Articulo
# modelo de facturas
from facturas.models import FacturaCompra
# modelo base de utilidades
from utilidades.base_name import BaseModel
# modelo de ventas
from ventas.models import Venta


class DetalleNotaCredito(BaseModel):
    """Modelo para detalle de nota de credito"""
    id_detalle_nota_credito = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)


class NotaCreditoCliente(BaseModel):
    """Modelo para Nota de credito de cliente"""
    id_nota_credito_cliente = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_detalle_nota_credito = models.ManyToManyField(DetalleNotaCredito, blank=False)
    fecha = models.DateField(default=date.today)
    monto_total = models.PositiveIntegerField(default=0)


class DetalleNotaCreditoProveedor(BaseModel):
    """Modelo de detalle de nota de credito de proveedor"""
    id_detalle_nota_credito_proveedor = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)
    costo_unitario = models.PositiveIntegerField(default=0)
    subtotal = models.PositiveIntegerField(default=0)


class NotaCreditoProveedor(BaseModel):
    """Modelo de nota de credito de proveedor"""
    id_nota_credito_proveedor = models.AutoField(primary_key=True)
    id_factura_compra = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)
    id_detalle_nota_credito_proveedor = models.ManyToManyField(DetalleNotaCreditoProveedor, blank=False)
    fecha = models.DateField(default=date.today)
    monto_total = models.PositiveIntegerField(default=0)
