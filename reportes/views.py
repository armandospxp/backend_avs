import pdb
from datetime import date, datetime

from django.db.models import Sum, Count
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from reportes.serializers import ReporteArticulosVendidos
from ventas.models import DetalleVenta


class ReporteArticulosMasVendidos(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ReporteArticulosVendidos

    def list(self, request):
        query = DetalleVenta.objects.all().values('id_articulo__nombre', 'sub_total').annotate(total=Sum('sub_total')).annotate(cantidad_vendida=Count('id_articulo__nombre')).order_by('-cantidad_vendida')[:5]
        serializer = ReporteArticulosVendidos(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
