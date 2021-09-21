from django.contrib.auth.models import Group, Permission
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from roles.models import Modulo, Rol, Permiso
from roles.serializers import GroupModelSerializer, PermisosModelSerializer, ModuloModelSerializer


class RolList(APIView):
    """Lista, crea, actualiza o elimina todos los grupos"""
    serializer_class = GroupModelSerializer

    def get(self, request, format=None):
        group = Rol.objects.all()
        serializer = GroupModelSerializer(group)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GroupModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolDetail(APIView):
    """Vista para update, delete, view detallado de un rol en especifico"""

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

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
    serializer_class = PermisosModelSerializer

    def get(self, request):
        permission = Permiso.objects.all()
        serializer = PermisosModelSerializer(permission)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PermisosModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModuloListView(APIView):
    serializer_class = ModuloModelSerializer

    def get(self, request):
        modulo = Modulo.objects.all()
        serializer = ModuloModelSerializer(modulo)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ModuloModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)