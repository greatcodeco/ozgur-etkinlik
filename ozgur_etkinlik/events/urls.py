from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name="event-list"),
    path('event-create/', views.event_create, name="event-create"),
    path('profile/', views.profile, name="profile"),
    path('event-update/<slug:slug>', views.event_update, name="event-update"),
    path('event-delete/<slug:slug>', views.event_delete, name="event-delete"),
    path('event-detail/<slug:slug>', views.event_detail, name="event-detail"),
    path('registerEvent/<int:id>', views.registerEvent, name="registerEvent"),
]
