from django.urls import path
from verification import views

urlpatterns = [
    path('email/request/', views.request_email_verification, name='request-email-verification'),
    path('sms/request/', views.request_sms_verification, name='request-sms-verification'),
    path('email/verify/', views.verify_email, name='verify-email'),
    path('sms/verify/', views.verify_sms, name='verify-sms'),
]
