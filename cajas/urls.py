from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from cajas.views import CajaList, CajaDetail

urlpatterns = format_suffix_patterns([
    path('', CajaList.as_view(), name='caja'),
    path('<int:pk>/', CajaDetail.as_view(), name='caja_detail'),
])
