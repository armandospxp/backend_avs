from django.http import Http404
from rest_framework import status, mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from proveedores.models import Proveedor
from proveedores.serializers import ProveedorModelSerializer


class MyPaginationMixin(object):
    pagination_class = PageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class ProveedorDetail(APIView):
    """
    Retorna, actualiza o borra una instancia de Caja.
    """
    serializer_class = ProveedorModelSerializer

    def get_object(self, pk):
        try:
            return Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        persona = self.get_object(pk)
        serializer = ProveedorModelSerializer(persona)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        persona = self.get_object(pk)
        serializer = ProveedorModelSerializer(persona, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        caja = self.get_object(pk)
        caja.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProveedorList(APIView, MyPaginationMixin):
    """Lista los articulos o los crea"""
    serializer_class = ProveedorModelSerializer

    def get(self, request, format=None):
        persona = Proveedor.objects.all()
        page = self.paginate_queryset(persona)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(persona, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # cliente = request["id_cliente"]
        serializer = ProveedorModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProveedorSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Proveedor.objects.filter(estado_activo="V")
    serializer_class = ProveedorModelSerializer
    search_fields = ['id_proveedor',
                     'tipo_persona',
                     'propietario',
                     'direccion',
                     'telefono',
                     'ruc',
                     'correo_electronico',
                     'fecha_nacimiento',
                     'estado_activo']
