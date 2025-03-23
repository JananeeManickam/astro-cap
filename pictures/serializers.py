# serializers.py
from rest_framework import serializers
from .models import TelescopeObservation, TelescopeStatus

class TelescopeObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelescopeObservation
        fields = '__all__'

class TelescopeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelescopeStatus
        fields = '__all__'