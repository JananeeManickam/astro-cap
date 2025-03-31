from django.contrib import admin
from .models import AstronomicalEvent

@admin.register(AstronomicalEvent)
class AstronomicalEventAdmin(admin.ModelAdmin):
    list_display = ['date', 'event_type', 'year']
    list_filter = ['event_type', 'date']
    search_fields = ['event_description']