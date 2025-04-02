from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import google_login_callback, validate_google_token, UserCreate, UserDetailView
from authentication.views import google_callback, google_login
urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication Endpoints
    path('api/auth/register/', UserCreate.as_view(), name='user_create'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/user/', UserDetailView.as_view(), name='user_detail'),
    # path('api/auth/google/callback/', google_login_callback, name='google_callback'),
    # path('api/auth/google/validate/', validate_google_token, name='validate_google_token'),
    
    # Include App Routes
    path('api/auth/google/callback/', google_callback, name='google_callback'),
    path('api/auth/google/login/', google_login, name='google_login'),
    path('api/auth/', include('authentication.urls')),
    path('api/users/', include('users.urls')),
    path('api/pictures/', include('pictures.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/onthisdate/', include('onthisdate.urls')),
    path('api/verification/', include('verification.urls')),
    path('api/', include('news.urls')),
    path('api/', include('chat.urls')),
]
