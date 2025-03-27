# from rest_framework import serializers
# from .models import ChatSession, ChatMessage

# class ChatMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatMessage
#         fields = ['is_user', 'content', 'created_at']

# class ChatSessionSerializer(serializers.ModelSerializer):
#     messages = ChatMessageSerializer(many=True, read_only=True)

#     class Meta:
#         model = ChatSession
#         fields = ['id', 'created_at', 'messages']

from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['message', 'is_user', 'timestamp']