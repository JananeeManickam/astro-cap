import datetime
from rest_framework import serializers
from authentication.models import SocialAccount

class SocialAccountSerializer(serializers.Serializer):
    user = serializers.CharField()
    provider = serializers.CharField()
    provider_id = serializers.CharField()
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
    expires_at = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return SocialAccount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = datetime.utcnow()
        instance.save()
        return instance