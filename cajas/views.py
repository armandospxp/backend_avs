# python datetime
from datetime import date, datetime
# django
from django.db.models import Sum
# rest-framework
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# modelos de cajas
from cajas.models import ArqueoCaja, MovimientoCaja, RetiroDineroCaja
# serializadores de cajas
from cajas.serializers import ArqueoCajaModelSerializer, MovimientoCajaModelSerializer, RetiroDineroCajaModelSerializer


class ArqueoCajaView(viewsets.ModelViewSet):
    """
        ViewSet de ArqueoCaja
        """
    serializer_class = ArqueoCajaModelSerializer
    queryset = ArqueoCaja.objects.order_by('-id_arqueo_caja')
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Listado de arqueo de cajas
        Si el usuario tiene rol administrador puede ver todos los arqueos, sino el ususario podra visualizar solo
        los arqueos que el haya creado"""
        if request.user.rol_usuario.upper() != 'ADMINISTRADOR':
            query = ArqueoCaja.objects.order_by('-id_arqueo_caja').filter(id_empleado=request.user)
        else:
            query = self.filter_queryset(self.get_queryset())
        queryset = query

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Crear un arqueo de caja"""
        data = request.data
        datos_modificados = data.copy()
        datos_modificados['id_empleado'] = int(request.user.pk)
        serializer = ArqueoCajaModelSerializer(data=datos_modificados)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Vista para actualizar monto comprobante"""
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
        """Vista para cerrar un arqueo de caja"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        datos = data.copy()
        datos['fecha_cierre'] = date.today()
        datos['hora_cierre'] = datetime.now().time().strftime("%H:%M:%S")
        fecha_inicio = datos['fecha_apertura']
        fecha_fin = datos['fecha_cierre']
        movimientos_dia = dict(
            MovimientoCaja.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).filter(
                id_empleado=instance.id_empleado).aggregate(Sum('monto')))
        suma_movimientos = movimientos_dia['monto__sum']
        comprobantes = dict(
            RetiroDineroCaja.objects.filter(id_arquero_caja=instance).aggregate(Sum('monto_comprobante')))
        if comprobantes == {} or comprobantes is None:
            suma_comprobantes = 0
        else:
            suma_comprobantes = comprobantes['monto_comprobante__sum']
        if suma_comprobantes is None:
            suma_comprobantes = 0
        if suma_movimientos is None:
            suma_movimientos = 0
        datos['monto_calculado'] = int(datos['monto_apertura']) + (int(suma_movimientos)) - suma_comprobantes
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


class RetiroDineroCajaView(viewsets.ModelViewSet):
    """
        ViewSet de RetiroDineroCaja
        """
    serializer_class = RetiroDineroCajaModelSerializer
    queryset = RetiroDineroCaja.objects.all()
    permission_classes = [IsAuthenticated]


class ArqueoCajaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """Vista para la busqueda de arqueo de cajas"""
    filter_backends = [SearchFilter]
    queryset = ArqueoCaja.objects.filter()
    serializer_class = ArqueoCajaModelSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id_empleado__first_name',
                     'id_empleado__last_name',
                     'id_arqueo_caja']


class MovimientoCajaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """Vista para la busqueda de movimiento de cajas"""
    filter_backends = [SearchFilter]
    queryset = MovimientoCaja.objects.filter()
    serializer_class = MovimientoCajaModelSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id_movimiento_caja',
                     'id_empleado__first_name',
                     'id_empleado__last_name',
                     'tipo_movimiento',
                     'id_empleado__username']
