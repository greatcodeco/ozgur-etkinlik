from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.events, name="events"),
    path('event-create/', views.event_create, name="event-create"),
    path('profile/', views.profile, name="profile"),
    path('update/<slug:slug>', views.updateEvent, name="update"),
    path('delete/<slug:slug>', views.deleteEvent, name="delete"),
    path('event-detail/<slug:slug>', views.event_detail, name="event-detail"),
    path('registerEvent/<int:id>', views.registerEvent, name="registerEvent"),
]
