from django.urls import path, include
from rest_framework import routers
from compras import views as compras_views

router = routers.DefaultRouter()
router.register(r'orden-compras', compras_views.OrdenCompraView, basename='orden-compras')

urlpatterns = [
    path('', include(router.urls)),
]