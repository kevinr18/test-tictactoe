# tictactoe_users/urls.py
from django.urls import path

from .views import UserLogin, UserCreate, UserLogout


urlpatterns = [
    path('users/', UserCreate.as_view(), name='user-create'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
]