"""Main URLs module."""

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
                  # Django Admin
                  path('admin/', admin.site.urls),
                  path('articulos/', include(('articulos.urls', 'articulos'), namespace='articulos')),
                  path('marcas/', include(('marcas.urls', 'marcas'), namespace='marcas')),
                  path('roles/', include(('roles.urls', 'roles'), namespace='roles')),
                  path('', include(('users.urls', 'users'), namespace='users')),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
