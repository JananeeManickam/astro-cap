from mongoengine import Document, StringField, ReferenceField, BooleanField, DateTimeField
from datetime import datetime, timedelta
import uuid
from users.models import User

class Verification(Document):
    user = ReferenceField(User, required=True)
    verification_type = StringField(choices=['email', 'sms'], required=True)
    token = StringField(default=lambda: str(uuid.uuid4()), required=True)
    is_verified = BooleanField(default=False)
    expires_at = DateTimeField(default=lambda: datetime.utcnow() + timedelta(days=3))
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'verifications'}
