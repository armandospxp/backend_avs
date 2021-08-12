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
    def user_update(self, request, username):
        """User update"""
        user = User.objects.get(username=username)
        serializer = UserUpdateSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.update(user, request.data)
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def user_delete(self, username):
        """User delete"""
        user = User.objects.get(username=username)
        user.delete()
        return Response({}, status=status.HTTP_200_OK)


class GroupList(APIView):
    """Lista, crea, actualiza o elimina todos los grupos"""

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, format=None):
        group = Group.objects.all()
        serializer = GroupModelSerializer(group)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupModelSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionList(APIView):
    """Lista todos los permisos"""

    def get(self, request):
        permission = Permission.objects.all()
        serializer = PermisosModelSerializer(permission)
        return Response(serializer.data)
