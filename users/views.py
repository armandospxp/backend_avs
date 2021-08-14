"""Users views."""

# Django REST Framework
from django.contrib.auth.models import Group, Permission
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from rest_framework.views import APIView

from users.serializers import UserLoginSerializer, UserModelSerializer, UserUpdateSerializer, GroupModelSerializer, \
    PermisosModelSerializer

# Models
from users.models import User

from users.serializers import UserSignUpSerializer


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
        data = {
            'users': UserModelSerializer(user).data,
            'access_token': token
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

    @action(detail=False, methods=['get'])
    def user_list(self, request):
        """User list"""
        user = User.objects.all()
        serializer = UserModelSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """User Update"""

    @action(detail=False, methods=['get'])
    def user_update(self, request):
        """User update"""
        username = request.GET.get('username', '')
        user = User.objects.get(username=username)
        serializer = UserUpdateSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.update(user, request.data)
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def user_delete(self, request):
        """User delete"""
        username = request.GET.get('username','')
        user = User.objects.get(username=username)
        user.delete()
        return Response({}, status=status.HTTP_200_OK)
