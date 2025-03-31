from rest_framework import serializers
from .models import AstronomicalEvent

class AstronomicalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomicalEvent
        fields = ['date', 'event_description', 'event_type', 'year']