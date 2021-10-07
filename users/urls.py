"""Users URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

# Views
from users import views as user_views


router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/', user_views.UserDetail.as_view(), name='user_detail'),
    path('users/', user_views.UserList.as_view(), name='user_detail'),
    path('users/busqueda/', user_views.UserSearchViewSet.as_view({'get': 'list'}), name='user_detail'),
    path('users/cambiopassword/<int:pk>/', user_views.UserUpdatePasswordView.as_view(), name='user_change_password12'),
]