from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name="events"),
    path('addevent/', views.addevent, name="addevent"),
    path('profile/', views.profile, name="profile"),
    path('update/<slug:slug>', views.updateEvent, name="update"),
    path('delete/<slug:slug>', views.deleteEvent, name="delete"),
    path('event/<slug:slug>', views.detail, name="detail"),
    path('registerEvent/<int:id>', views.registerEvent, name="registerEvent"),
]
