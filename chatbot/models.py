# from django.db import models
# import uuid

# class ChatSession(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)

# class ChatMessage(models.Model):
#     session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
#     is_user = models.BooleanField(default=True)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['created_at']

from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    """
    Model to store chat messages for session tracking
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_user = models.BooleanField(default=True)  # True for user message, False for bot response
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40)  # To track specific chat sessions

    class Meta:
        ordering = ['timestamp']