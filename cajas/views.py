from rest_framework import status, viewsets

from cajas.models import Caja, ArqueoCaja, MovimientoCaja
from cajas.serializers import CajaModelSerializer, ArqueoCajaModelSerializer, MovimientoCajaModelSerializer


class CajaView(viewsets.ModelViewSet):
    """
    ViewSet de Caja
    """
    serializer_class = CajaModelSerializer
    queryset = Caja.objects.all()


class ArqueoCajaView(viewsets.ModelViewSet):
    """
        ViewSet de ArqueoCaja
        """
    serializer_class = ArqueoCajaModelSerializer
    queryset = ArqueoCaja.objects.all()


class MovimientoCajaView(viewsets.ModelViewSet):
    """
        ViewSet de MovimientoCaja
        """
    serializer_class = MovimientoCajaModelSerializer
    queryset = MovimientoCaja.objects.all()
