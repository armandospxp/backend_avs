"""Users URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from articulos import views as articulo_views

router = DefaultRouter()
router.register(r'users', articulo_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]