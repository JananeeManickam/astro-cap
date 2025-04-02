from rest_framework import serializers
from verification.models import Verification

class VerificationSerializer(serializers.Serializer):
    user = serializers.CharField()
    verification_type = serializers.CharField()
    token = serializers.CharField()
    is_verified = serializers.BooleanField(default=False)
    expires_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
