from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from roles.views import RolList, PermissionList

urlpatterns = format_suffix_patterns([
    path('', RolList.as_view(), name='roles'),
    path('permisos/', PermissionList.as_view(), name='permisos'),
])