from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    logout_user,
    register_user,
    reset_password,
    reset_password_confirm,
    CustomTokenObtainPairView
)


urlpatterns = [
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token-obtain'),
    path('users/logout/', logout_user, name='logout'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('users/register/', register_user, name='user-register'),
    path('users/reset_password/',
         reset_password, name='reset-password'),
    path('users/reset_password_confirm/',
         reset_password_confirm, name='reset-password-confirm'),
]
