from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from cajas.models import Caja
from cajas.serializers import CajaModelSerializer


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


class CajaDetail(APIView):
    """
    Retorna, actualiza o borra una instancia de Caja.
    """
    serializer_class = CajaModelSerializer

    def get_object(self, pk):
        try:
            return Caja.objects.get(pk=pk)
        except Caja.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        caja = self.get_object(pk)
        serializer = CajaModelSerializer(caja)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        caja = self.get_object(pk)
        serializer = CajaModelSerializer(caja, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        caja = self.get_object(pk)
        caja.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CajaList(APIView, MyPaginationMixin):
    """Lista los articulos o los crea"""
    serializer_class = CajaModelSerializer

    def get(self, request, format=None):
        articulo = Caja.objects.all()
        page = self.paginate_queryset(articulo)
        serializer = CajaModelSerializer(articulo, many=True)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(articulo, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CajaModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
