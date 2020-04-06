

from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



app_name = 'users'

urlpatterns = [
    path('', views.UsersHome.as_view(), name='homepage'),
    path('registration/', views.UserCreateView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('update/', views.UserUpdateView.as_view(), name='employee_update'),
]
