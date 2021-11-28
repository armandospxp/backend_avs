from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from configuracion.models import Configuracion
from configuracion.serializers import ConfiguraionModelSerializer


class ConfiguraiconView(viewsets.ModelViewSet):
    serializer_class = ConfiguraionModelSerializer
    queryset = Configuracion.objects.all()


class ConfiguracionSearchViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [SearchFilter]
    queryset = Configuracion.objects.filter()
    serializer_class = ConfiguraionModelSerializer
    search_fields = ['nombre_impresora',
                     'numeracion_fija_factura',
                     ]

# class ConfiguracionDetail(APIView):
#     """
#     Retorna, actualiza o borra una instancia de Caja.
#     """
#     serializer_class = ConfiguraionModelSerializer
#
#     def get_object(self, pk):
#         try:
#             return Configuracion.objects.get(pk=pk)
#         except Configuracion.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         caja = self.get_object(pk)
#         serializer = ConfiguraionModelSerializer(caja)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         caja = self.get_object(pk)
#         serializer = ConfiguraionModelSerializer(caja, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         caja = self.get_object(pk)
#         caja.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class ConfiguracionList(APIView):
#     """Lista los articulos o los crea"""
#     serializer_class = ConfiguraionModelSerializer
#
#     def get(self, request, format=None):
#         configuracion = Configuracion.objects.all()
#         serializer = ConfiguraionModelSerializer(configuracion, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ConfiguraionModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
