from django.http import Http404
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from personas.models import Persona
from personas.serializers import PersonaModelSerializers, PersonaListSerializer


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


class PerosnaDetail(APIView):
    """
    Retorna, actualiza o borra una instancia de Caja.
    """
    serializer_class = PersonaModelSerializers

    def get_object(self, pk):
        try:
            return Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        persona = self.get_object(pk)
        serializer = PersonaModelSerializers(persona)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        persona = self.get_object(pk)
        serializer = PersonaModelSerializers(persona, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        caja = self.get_object(pk)
        caja.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonaList(APIView, MyPaginationMixin):
    """Lista los articulos o los crea"""
    serializer_class = PersonaModelSerializers

    def get(self, request, format=None):
        persona = Persona.objects.all()
        page = self.paginate_queryset(persona)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(persona, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonaModelSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonaClienteList(APIView, MyPaginationMixin):
    """Lista los clientes"""
    serializer_class = PersonaModelSerializers

    def get(self, request, format=None):
        persona = Persona.objects.filter(es_cliente='V')
        page = self.paginate_queryset(persona)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(persona, many=True)
        return Response(serializer.data)


class PersonaProveedorList(APIView, MyPaginationMixin):
    """Lista los proveedores"""
    serializer_class = PersonaModelSerializers

    def get(self, request, format=None):
        persona = Persona.objects.filter(es_proveedor='V')
        page = self.paginate_queryset(persona)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(persona, many=True)
        return Response(serializer.data)


class PersonaSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Persona.objects.filter(estado_activo="V")
    serializer_class = PersonaModelSerializers
    search_fields = (
        '^id_persona',
        '^tipo_persona',
        '^nombre_apellido',
        '^propietario',
        '^direccion',
        '^telefono',
        '^ruc',
        '^cedula',
        '^correo_electronico',
        '^es_cliente',
        '^es_proveedor',
        '^fecha_nacimiento',
        '^estado_activo',
    )


class PersonaProveedorSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Persona.objects.filter(estado_activo="V", es_proveedor='V')
    serializer_class = PersonaModelSerializers
    search_fields = (
        'id_persona',
        'tipo_persona',
        'nombre_apellido',
        'propietario',
        'direccion',
        'telefono',
        'ruc',
        'cedula',
        'correo_electronico',
        'es_cliente',
        'es_proveedor',
        'fecha_nacimiento',
        'estado_activo',
    )


@api_view(('GET',))
def personas_lista_sin_paginacion(request, format=None):
    personas = Persona.objects.filter(es_cliente='V')
    serializer = PersonaModelSerializers(personas, many=True)
    return Response(serializer.data)


@api_view(('GET',))
def personas_proveedor_sin_paginacion(request, format=None):
    personas = Persona.objects.filter(es_proveedor='V')
    serializer = PersonaModelSerializers(personas, many=True)
    return Response(serializer.data)
