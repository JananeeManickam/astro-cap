import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import User
from authentication.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
@permission_classes([AllowAny])
def google_login(request):
    print("se consistent redirect URI that matches your Google OAuth configuration")
    # Use consistent redirect URI that matches your Google OAuth configuration
    redirect_uri = f"{settings.BASE_URL}/api/auth/google/callback/"
    
    return Response({
        "auth_url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&scope=email%20profile&access_type=offline"
    })

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return Response({"error": "Authorization code not provided"}, status=400)
    
    # Use consistent redirect URI
    redirect_uri = f"{settings.BASE_URL}/api/auth/google/callback/"
    
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
    if token_response.status_code != 200:
        return Response({"error": f"Failed to obtain access token: {token_response.text}"}, status=400)
    
    tokens = token_response.json()
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    expires_in = tokens.get('expires_in')
    
    user_info_response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    if user_info_response.status_code != 200:
        return Response({"error": "Failed to fetch user data"}, status=400)
    
    user_info = user_info_response.json()
    email = user_info.get('email')
    google_id = user_info.get('sub')
    
    # Try to get the user, if not create one
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User(
            email=email,
            first_name=user_info.get('given_name', ''),
            last_name=user_info.get('family_name', ''),
            level='beginner'
        )
        user.save()
    
    # Update or create social account
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        social_account.access_token = access_token
        social_account.refresh_token = refresh_token if refresh_token else social_account.refresh_token
        social_account.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        social_account.save()
    except SocialAccount.DoesNotExist:
        SocialAccount.objects.create(
            user=user,
            provider='google',
            provider_id=google_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(seconds=expires_in)
        )
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    # Redirect with the token
    return redirect(f"{settings.BASE_URL}/api/pictures/?token={str(refresh.access_token)}")