from django.contrib.auth.backends import BaseBackend
from users.models import User

class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, email=None):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None