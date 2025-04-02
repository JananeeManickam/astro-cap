import datetime
from rest_framework import serializers
from chat.models import ChatRoom, Message
from users.serializers import UserSerializer

class ChatRoomSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False)
    members = serializers.ListField(child=serializers.CharField(), required=False)
    created_by = serializers.CharField()
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return ChatRoom.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = datetime.utcnow()
        instance.save()
        return instance

class MessageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    room = serializers.CharField()
    sender = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = datetime.utcnow()
        instance.save()
        return instance