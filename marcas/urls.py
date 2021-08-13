from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from articulos.views import MarcaList, MarcaDetail

urlpatterns = format_suffix_patterns([
    path('', MarcaList.as_view(), name='marcas'),
    path('<pk>/', MarcaDetail.as_view(), name='marca'),
])