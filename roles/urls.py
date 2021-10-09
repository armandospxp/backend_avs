from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from roles.views import RolView, PermisoView, ModuloView
from rest_framework import routers

# from roles.views import RolList, RolDetail, PermissionList, ModuloListView

# urlpatterns = format_suffix_patterns([
#     path('roles/', RolList.as_view(), name='roles'),
#     path('roles/<pk>/', RolDetail.as_view(), name='roles_detalles'),
#     path('permisos/', PermissionList.as_view(), name='permisos'),
#     path('modulos/', ModuloListView.as_view(), name='modulos')
# ])

router = routers.DefaultRouter()
router.register('roles', RolView)
router.register('modulos', ModuloView)
router.register('permisos', PermisoView)

urlpatterns = [
    path('', include(router.urls))
]