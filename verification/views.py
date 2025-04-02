from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from verification.models import Verification
from verification.utils import send_email_verification, send_sms_verification

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_email_verification(request):
    user = request.user

    existing = Verification.objects.filter(
        user=user,
        verification_type='email',
        expires_at__gt=datetime.utcnow(),
        is_verified=False
    ).first()

    if existing:
        return Response({"message": "A verification email was already sent."})

    verification = send_email_verification(user)
    return Response({"message": "Verification email sent successfully."})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_sms_verification(request):
    user = request.user
    phone_number = request.data.get('phone_number')

    if not phone_number:
        return Response({"error": "Phone number is required."}, status=400)

    existing = Verification.objects.filter(
        user=user,
        verification_type='sms',
        expires_at__gt=datetime.utcnow(),
        is_verified=False
    ).first()

    if existing:
        return Response({"message": "A verification code was already sent."})

    verification = send_sms_verification(user, phone_number)
    return Response({"message": "Verification SMS sent successfully."})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.data.get('token')

    if not token:
        return Response({"error": "Verification token is required."}, status=400)

    try:
        verification = Verification.objects.get(
            token=token,
            verification_type='email',
            expires_at__gt=datetime.utcnow(),
            is_verified=False
        )
    except Verification.DoesNotExist:
        return Response({"error": "Invalid or expired verification token."}, status=400)

    verification.is_verified = True
    verification.save()

    return Response({"message": "Email verified successfully."})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_sms(request):
    phone_number = request.data.get('phone_number')
    code = request.data.get('code')

    if not phone_number or not code:
        return Response({"error": "Phone number and verification code are required."}, status=400)

    try:
        verification = Verification.objects.get(
            token=code,
            verification_type='sms',
            expires_at__gt=datetime.utcnow(),
            is_verified=False
        )
    except Verification.DoesNotExist:
        return Response({"error": "Invalid or expired verification code."}, status=400)

    verification.is_verified = True
    verification.save()

    return Response({"message": "Phone number verified successfully."})
