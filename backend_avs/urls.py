"""Modulo principa de URLs de todas los modulos."""

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
                  path('personas/', include(('personas.urls', 'personas'), namespace='personas')),
                  path('proveedores/', include(('proveedores.urls', 'proveedores'), namespace='proveedores')),
                  path('configuracion/', include(('configuracion.urls', 'configuracion'), namespace='configuracion')),
                  path('cajas/', include(('cajas.urls', 'cajas'), namespace='cajas')),
                  path('ventas/', include(('ventas.urls', 'ventas'), namespace='ventas')),
                  path('nota-credito/', include(('nota_credito.urls', 'nota-credito'), namespace='nota-credito')),
                  path('orden-compras/', include(('compras.urls', 'compras'), namespace='compras')),
                  path('facturas/', include(('facturas.urls', 'facturas'), namespace='facturas')),
                  path('reportes/', include(('reportes.urls', 'reportes'), namespace='reportes')),
                  path('', include(('users.urls', 'users'), namespace='users')),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
