from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="user-login"),
    path('logout/', views.user_logout, name="user-logout"),
]
