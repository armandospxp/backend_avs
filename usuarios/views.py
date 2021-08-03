"""Users views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from usuarios.serializers import UsuarioLoginSerializer, UsuarioModelSerializer

# Models
from usuarios.models import Usuario

from usuarios.serializers import UsuarioSignUpSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = Usuario.objects.filter(is_active=True)
    serializer_class = UsuarioModelSerializer

    # Detail define si es una petición de detalle o no, en methods añadimos el método permitido, en nuestro caso solo vamos a permitir post
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UsuarioLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UsuarioModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UsuarioSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UsuarioModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
