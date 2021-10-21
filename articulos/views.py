from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from articulos.serializers import ArticuloModelSerializer, MarcaModelSerializer
from articulos.models import Articulo, Marca


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


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


class ArticuloDetail(APIView):
    """
    Retorna, actualiza o borra una instancia de articulo.
    """
    serializer_class = ArticuloModelSerializer
    pagination_class = PageNumberPagination

    def get_object(self, pk):
        try:
            return Articulo.objects.get(pk=pk)
        except Articulo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        articulo = self.get_object(pk)
        page = self.paginate_queryset(articulo)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticuloModelSerializer(articulo)
        return Response(serializer.data)

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


class ArticuloList(APIView, MyPaginationMixin):
    """Lista los articulos o los crea"""
    serializer_class = ArticuloModelSerializer

    def get(self, request, format=None):
        articulo = Articulo.objects.all()
        page = self.paginate_queryset(articulo)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                                           many=True).data)
        else:
            serializer = self.serializer_class(articulo, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticuloModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarcaDetail(APIView, MyPaginationMixin):
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
        return Response(serializer.data)

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


class ArticuloSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Articulo.objects.filter()
    serializer_class = ArticuloModelSerializer
    search_fields = ['id_articulo',
                     'nombre',
                     'costo',
                     'id_marca',
                     'codigo_barras',
                     'porc_iva',
                     'porc_comision',
                     'stock_actual',
                     'stock_minimo',
                     'ultima_compra',
                     'unidad_medida',
                     'precio_unitario',
                     'precio_mayorista',
                     'precio_especial', ]
