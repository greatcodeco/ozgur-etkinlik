from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.event_list, name="event-list"),
    path('event-create/', views.event_create, name="event-create"),
    path('profile/', views.profile, name="profile"),
    path('event-update/<slug:slug>', views.event_update, name="event-update"),
    path('event-delete/<slug:slug>', views.event_delete, name="event-delete"),
    path('event-detail/<slug:slug>', views.event_detail, name="event-detail"),
    path('registerEvent/<int:id>', views.registerEvent, name="registerEvent"),

    url(r'^new-add-comment/(?P<pk>[0-9]+)/(?P<model_type>[\w]+)/$', views.new_add_comment, name='new-add-comment'),

    url(r'^get-child-comment-form/$', views.get_child_comment_form, name='get-child-comment-form'),

]
