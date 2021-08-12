from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from articulos.views import ArticuloList, ArticuloDetail, MarcaList, MarcaDetail

urlpatterns = format_suffix_patterns([
    path('', ArticuloList.as_view(), name='articulos'),
    path('<int:pk>/', ArticuloDetail.as_view(), name='articulo'),
    path('marcas/', MarcaList.as_view(), name='marcas'),
    path('marca/<int:pk>/', MarcaDetail.as_view(), name='marca'),
])