from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name = "events"),
    path('addevent/', views.addevent, name = "addevent"),
    path('profile/', views.profile, name = "profile"),
    path('update/<int:id>', views.updateEvent, name = "update"),
    path('delete/<int:id>', views.deleteEvent, name = "delete"),
    path('event/<int:id>', views.detail, name = "detail"),
    path('registerEvent/<int:id>', views.registerEvent, name = "registerEvent"),
 ]