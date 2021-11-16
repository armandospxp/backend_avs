from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from compras.serializers import OrdenCompraModelSerializer
from compras.models import OrdenCompra


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


class OrdenCompraView(viewsets.ModelViewSet):
    serializer_class = OrdenCompraModelSerializer
    queryset = OrdenCompra.objects.all()
