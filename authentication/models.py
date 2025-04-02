from mongoengine import Document, StringField, ReferenceField, BooleanField, DateTimeField
from datetime import datetime
from users.models import User

class SocialAccount(Document):
    user = ReferenceField(User, required=True)
    provider = StringField(choices=['google'], required=True)
    provider_id = StringField(required=True)
    access_token = StringField()
    refresh_token = StringField()
    expires_at = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'social_accounts'}
