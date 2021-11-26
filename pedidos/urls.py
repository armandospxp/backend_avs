from django.urls import path, include
from rest_framework import routers
from pedidos import views as pedidos_views

router = routers.DefaultRouter()
router.register(r'pedidos', pedidos_views.PedidoView, basename='pedidos')

urlpatterns = [
    path('', include(router.urls)),
]