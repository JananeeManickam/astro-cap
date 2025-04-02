import random
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
import requests
from verification.models import Verification
from users.models import User

def generate_token():
    """Generate a unique token for verification."""
    return str(uuid.uuid4())

def send_email_verification(user):
    """Create and send an email verification link to the user."""
    verification = Verification.objects.create(
        user=user,
        verification_type='email',
        token=generate_token(),
        expires_at=datetime.utcnow() + timedelta(days=3)
    )

    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification.token}"
    
    try:
        send_mail(
            'Verify Your Email',
            f'Click the link to verify your email: {verification_url}',
            settings.EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")

    return verification

def send_sms_verification(user, phone_number):
    """Generate and send an SMS verification code."""
    verification = Verification.objects.create(
        user=user,
        verification_type='sms',
        token="".join([str(random.randint(0, 9)) for _ in range(6)]),  # 6-digit code
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )

    # Placeholder for actual SMS sending logic, e.g., Twilio API
    # Example:
    # twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # message = twilio_client.messages.create(
    #     body=f'Your verification code is: {verification.token}',
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=phone_number
    # )

    print(f"SMS sent to {phone_number}: Code - {verification.token}")

    return verification
