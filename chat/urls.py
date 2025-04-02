from django.urls import path
from chat import views

urlpatterns = [
    path('chat/rooms/', views.chat_rooms, name='chat-rooms'),
    path('chat/rooms/<str:room_id>/', views.chat_room_detail, name='chat-room-detail'),
    path('chat/rooms/<str:room_id>/join/', views.join_chat_room, name='join-chat-room'),
    path('chat/rooms/<str:room_id>/leave/', views.leave_chat_room, name='leave-chat-room'),
    path('chat/rooms/<str:room_id>/messages/', views.room_messages, name='room-messages'),
]
