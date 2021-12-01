from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter

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


class CajaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Caja.objects.filter()
    serializer_class = CajaModelSerializer
    search_fields = ['id_caja',
                     'id_empleado__nombre_apellido',
                     'descripcion']


class ArqueoCajaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = ArqueoCaja.objects.filter()
    serializer_class = ArqueoCajaModelSerializer
    search_fields = ['id_caja',
                     'id_empleado__nombre_apellido',
                     'id_arqueo_caja']


class MovimientoCajaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = MovimientoCaja.objects.filter()
    serializer_class = MovimientoCajaModelSerializer
    search_fields = ['id_movimiento_caja',
                     'id_empleado__nombre_apellido',
                     'tipo_movimiento']

