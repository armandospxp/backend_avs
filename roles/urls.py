# django
from django.urls import path, include
# app de roles
from roles.views import RolView, PermisoView, ModuloView
# rest-framework routers
from rest_framework import routers

router = routers.DefaultRouter()
router.register('roles', RolView)
router.register('modulos', ModuloView)
router.register('permisos', PermisoView)

"""Urls de roles"""
urlpatterns = [
    path('', include(router.urls))
]
