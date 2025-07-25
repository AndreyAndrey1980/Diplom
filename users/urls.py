from django.urls import path

from .views import reset_password, reset_password_confirm


urlpatterns = [
    path('users/reset_password/',
         reset_password, name='reset-password'),
    path('users/reset_password_confirm/',
         reset_password_confirm, name='reset-password-confirm'),
]
