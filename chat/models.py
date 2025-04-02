from mongoengine import Document, StringField, ReferenceField, ListField, DateTimeField
from datetime import datetime
from users.models import User

class ChatRoom(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=500)
    members = ListField(ReferenceField(User))
    created_by = ReferenceField(User, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'chat_rooms'}

class Message(Document):
    room = ReferenceField(ChatRoom, required=True)
    sender = ReferenceField(User, required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'messages'}