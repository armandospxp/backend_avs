from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from personas.views import PersonaList, PerosnaDetail

urlpatterns = format_suffix_patterns([
    path('', PersonaList.as_view(), name='configuracion'),
    path('<int:pk>/', PerosnaDetail.as_view(), name='configuracion_detail'),
])
