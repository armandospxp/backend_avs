# rest framework
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
# modelo de configuracion
from configuracion.models import Configuracion
# serialziador de configruacion
from configuracion.serializers import ConfiguraionModelSerializer


class ConfiguraiconView(viewsets.ModelViewSet):
    """ViewSet de Configuracion"""
    serializer_class = ConfiguraionModelSerializer
    queryset = Configuracion.objects.all()


class ConfiguracionSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de busqueda de configuracion"""
    filter_backends = [SearchFilter]
    queryset = Configuracion.objects.filter()
    serializer_class = ConfiguraionModelSerializer
    search_fields = ['nombre_impresora',
                     'numeracion_fija_factura',
                     ]


@api_view(('GET',))
def configuracion_lista_sin_paginacion(request, format=None):
    """Lista de configuracion para input"""
    configuracion = Configuracion.objects.filter()
    serializer = ConfiguraionModelSerializer(configuracion, many=True)
    return Response(serializer.data)
