from django.contrib.auth.models import Group, Permission
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from roles.serializers import GroupModelSerializer, PermisosModelSerializer


class RolList(APIView):
    """Lista, crea, actualiza o elimina todos los grupos"""
    serializer_class = GroupModelSerializer

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        group = Group.objects.values_list('id', 'name', 'permissions')
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
    serializer_class = PermisosModelSerializer

    def get(self, request):
        permission = Permission.objects.values_list('id')
        serializer = PermisosModelSerializer(permission)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PermisosModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        permiso = self.get_object(pk)
        serializer = PermisosModelSerializer(permiso, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        permiso = self.get_object(pk)
        permiso.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
