from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from configuracion.views import ConfiguracionList, ConfiguracionDetail

urlpatterns = format_suffix_patterns([
    path('', ConfiguracionList.as_view(), name='configuracion'),
    path('<int:pk>/', ConfiguracionDetail.as_view(), name='configuracion_detail'),
])
