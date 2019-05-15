from django.contrib import admin

from .models import Event, EventMember

# Register your models here.

admin.site.register(EventMember)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date", "slug"]
    list_display_links = ["title", "created_date"]

    search_fields = ["title"]

    list_filter = ["created_date"]

    class Meta:
        model = Event
