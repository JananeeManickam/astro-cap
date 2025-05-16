# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ChatbotViewSet

# router = DefaultRouter()
# router.register(r'chat', ChatbotViewSet, basename='chat')

# urlpatterns = [
#     path('', include(router.urls)),
# ]


from django.urls import path
from chatbot.views import AstronomyChatbotView

urlpatterns = [
    path('chat/', AstronomyChatbotView.as_view(), name='astronomy-chatbot'),
]