"""Users views."""

# Django REST Framework
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Serializers
from rest_framework.views import APIView

from users.serializers import UserLoginSerializer, UserModelSerializer, UserUpdateSerializer, UserUpdatePassword

# Models
from users.models import User

from users.serializers import UserSignUpSerializer


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


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    # Detail define si es una petición de detalle o no, en methods añadimos el método permitido, en nuestro caso solo vamos a permitir post
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        rol = str(user.rol_usuario)
        if rol.upper() == 'CAJERO' and user.configuracion is not None:
            impresora = str(user.configuracion.nombre_impresora)
            coordenada_x = str(user.configuracion.coordenada_x)
            coordenada_y = str(user.configuracion.coordenada_y)
            data = {
                'users': UserModelSerializer(user).data,
                'access_token': token,
                'id_configuracion': str(user.configuracion.id_impresora),
                'nombre_impresora': impresora,
                'coordenada_x': coordenada_x,
                'coordenada_y': coordenada_y,
            }
        else:
            data = {
                'users': UserModelSerializer(user).data,
                'access_token': token,
                'id_configuracion': 0,
                'coordenada_x': 0,
                'coordenada_y': 0,
            }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class UserList(APIView, MyPaginationMixin):
    """Clase para listar usuarios"""
    serializer_class = UserModelSerializer

    def get(self, request, format=None):
        user = User.objects.all()
        page = self.paginate_queryset(user)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retorna, actualiza o borra una instancia de Caja.
    """
    serializer_class = UserModelSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserModelSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    search_fields = (
        '^username',
        '^first_name',
        '^last_name',
        '^email',
    )


class UserUpdatePasswordView(APIView):

    serializer_class = UserUpdatePassword

    def put(self, request, pk, format=None):
        print(pk)
        user = User.objects.get(id=pk)
        serializer = UserUpdatePassword(data=request.data)
        if serializer.is_valid(self):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
