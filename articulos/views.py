from django.http import Http404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from articulos.serializers import ArticuloModelSerializer, MarcaModelSerializer
from articulos.models import Articulo, Marca


class ArticuloDetail(APIView, PageNumberPagination):
    """
    Retorna, actualiza o borra una instancia de articulo.
    """
    serializer_class = ArticuloModelSerializer

    def get_object(self, pk):
        try:
            return Articulo.objects.get(pk=pk)
        except Articulo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        articulo = self.get_object(pk)
        articulo_paginated = self.paginate_queryset(articulo, view=self)
        serializer = ArticuloModelSerializer(articulo_paginated)
        return self.get_paginated_response(serializer.data)

    def put(self, request, pk, format=None):
        articulo = self.get_object(pk)
        serializer = ArticuloModelSerializer(articulo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        articulo = self.get_object(pk)
        articulo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticuloList(APIView):
    """Lista los articulos o los crea"""
    serializer_class = ArticuloModelSerializer

    def get(self, request, format=None):
        articulo = Articulo.objects.all()
        articulo_paginated = self.paginate_queryset(articulo, view=self)
        serializer = ArticuloModelSerializer(articulo_paginated, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticuloModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarcaDetail(APIView):
    """
    Retorna, actualiza o borra una instancia de marca.
    """
    serializer_class = MarcaModelSerializer

    def get_object(self, pk):
        try:
            return Marca.objects.get(pk=pk)
        except Marca.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        marca = self.get_object(pk)
        serializer = MarcaModelSerializer(marca)
        return self.get_paginated_response(serializer.data)

    def put(self, request, pk, format=None):
        marca = self.get_object(pk)
        serializer = ArticuloModelSerializer(marca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        marca = self.get_object(pk)
        marca.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MarcaList(APIView):
    """Lista las marcas o los crea"""

    serializer_class = MarcaModelSerializer

    def get(self, request, format=None):
        marca = Marca.objects.all()
        serializer = MarcaModelSerializer(marca, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MarcaModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
