# modelo de users
from users.models import User
# rest-framework
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
# modelo de roles
from roles.models import Modulo, Rol, Permiso
from roles.serializers import RolModelSerializer, PermisosModelSerializer, ModuloModelSerializer


class MyPaginationMixin(object):
    """Paginacion para roles"""
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


class RolView(viewsets.ModelViewSet):
    """Vista de roles"""
    serializer_class = RolModelSerializer
    queryset = Rol.objects.all()

    def get_queryset(self):
        """Obtener todos los roles"""
        rol = Rol.objects.all()
        return rol

    def create(self, request, *args, **kwargs):
        """Crear rol"""
        data = request.data
        nuevo_rol = Rol.objects.create(nombre_rol=data["nombre_rol"])
        nuevo_rol.save()
        for user in data["usuario"]:
            user_object = User.objects.get(id=user["id"])
            nuevo_rol.usuario.add(user_object)
        for modulo in data["modulo"]:
            modulo_object = Modulo.objects.get(id_modulo=modulo["id_modulo"])
            nuevo_rol.modulo.add(modulo_object)

        serializer = RolModelSerializer(nuevo_rol)

        return Response(serializer.data)


class ModuloView(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloModelSerializer


class PermisoView(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisosModelSerializer


class RolesSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """Buscador de roles"""
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
        '^id_modulo',
        '^nombre_modulo',
    )


class PermisoSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Permiso.objects.all()
    serializer_class = PermisosModelSerializer
    search_fields = (
        'id_permiso',
        'descripcion',
    )
