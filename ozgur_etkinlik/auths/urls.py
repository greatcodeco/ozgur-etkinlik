from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('user-profile-update/', views.user_profile_update, name='user-profile-update'),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="user-login"),
    path('logout/', views.user_logout, name="user-logout"),
    path('logout/', views.user_logout, name="user-logout"),
    path('<str:username>/', views.user_profile, name="user-profile"),
    path('profile-list-events', views.profile_list_events, name="profile-list-events"),
]
