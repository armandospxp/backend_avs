import pdb
from datetime import date, datetime

from django.db.models import Sum
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cajas.models import ArqueoCaja, MovimientoCaja
from cajas.serializers import ArqueoCajaModelSerializer, MovimientoCajaModelSerializer


class ArqueoCajaView(viewsets.ModelViewSet):
    """
        ViewSet de ArqueoCaja
        """
    serializer_class = ArqueoCajaModelSerializer
    queryset = ArqueoCaja.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        datos_modificados = data.copy()
        datos_modificados['id_empleado'] = int(request.user.pk)
        serializer = ArqueoCajaModelSerializer(data=datos_modificados)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        # kwargs['partial'] = True
        data = request.data
        datos = data.copy()
        if datos == {} or datos is None:
            error = {'error': 'No puede enviar datos vacios'}
            return Response(error, status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        datos['monto_comprobante'] = int(datos['monto_comprobante']) + int(instance.monto_comprobante)
        serializer = self.get_serializer(instance, data=datos, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        datos = data.copy()
        datos['fecha_cierre'] = date.today()
        datos['hora_cierre'] = datetime.now().time().strftime("%H:%M:%S")
        fecha_inicio = datos['fecha_apertura']
        fecha_fin = datos['fecha_cierre']
        movimientos_dia = dict(
            MovimientoCaja.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(Sum('monto')))
        suma_movimientos = movimientos_dia['monto__sum']
        suma_comprobantes = int(datos['monto_comprobante'])
        datos['monto_calculado'] = int(datos['monto_cierre']) - (int(suma_movimientos) + suma_comprobantes)
        serializer = self.get_serializer(instance, data=datos, partial=partial)
        serializer.is_valid(raise_exception=True)
        # datos = dict(serializer.data)
        # serializer.data = datos
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class MovimientoCajaView(viewsets.ModelViewSet):
    """
        ViewSet de MovimientoCaja
        """
    serializer_class = MovimientoCajaModelSerializer
    queryset = MovimientoCaja.objects.all()
    permission_classes = [IsAuthenticated]


class ArqueoCajaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = ArqueoCaja.objects.filter()
    serializer_class = ArqueoCajaModelSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id_empleado__first_name',
                     'id_empleado__last_name',
                     'id_arqueo_caja']


class MovimientoCajaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = MovimientoCaja.objects.filter()
    serializer_class = MovimientoCajaModelSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id_movimiento_caja',
                     'id_empleado__first_name',
                     'id_empleado__last_name',
                     'tipo_movimiento']
