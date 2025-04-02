from django.urls import path
from .views import SpaceNewsAPIView

urlpatterns = [
    path('space-news/', SpaceNewsAPIView.as_view(), name='space-news')
]
    