from django.contrib.auth.models import Group, Permission
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from roles.models import Modulo, Rol, Permiso
from roles.serializers import RolModelSerializer, PermisosModelSerializer, ModuloModelSerializer


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


class RolList(APIView, MyPaginationMixin):
    """Lista, crea, actualiza o elimina todos los grupos"""
    serializer_class = RolModelSerializer

    def get(self, request, format=None):
        group = Rol.objects.all()
        page = self.paginate_queryset(group)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(group, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RolModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolDetail(APIView):
    """Vista para update, delete, view detallado de un rol en especifico"""

    serializer_class = RolModelSerializer

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        rol = self.get_object(pk)
        serializer = RolModelSerializer(rol, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = RolModelSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionList(APIView, MyPaginationMixin):
    """Lista todos los permisos"""
    serializer_class = PermisosModelSerializer

    def get(self, request):
        permission = Permiso.objects.all()
        page = self.paginate_queryset(permission)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(permission, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PermisosModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModuloListView(APIView, MyPaginationMixin):
    serializer_class = ModuloModelSerializer

    def get(self, request):
        modulo = Modulo.objects.all()
        page = self.paginate_queryset(modulo)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(modulo, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ModuloModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolesSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Rol.objects.all()
    serializer_class = RolModelSerializer
    search_fields = (
        'id_rol',
        'nombre_rol',
        'usuario',
        'permiso',
        'modulo',
    )


class ModuloSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Modulo.objects.all()
    serializer_class = ModuloModelSerializer
    search_fields = (
        'id_modulo',
        'nombre_modulo',
    )


class PermisoSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Permiso.objects.all()
    serializer_class = PermisosModelSerializer
    search_fields = (
        'id_permiso',
        'descripcion',
    )
