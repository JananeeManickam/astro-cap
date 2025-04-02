from django.urls import path
from authentication.views import google_login, google_callback

urlpatterns = [
    path('google/login/', google_login, name='google-login'),
    path('google/callback/', google_callback, name='google-callback'),
]
