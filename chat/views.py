from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime

from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer
from users.models import User

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chat_rooms(request):
    if request.method == 'GET':
        # List rooms the user is a member of
        user = request.user
        rooms = ChatRoom.objects.filter(members=user)
        serializer = ChatRoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create a new room
        data = request.data.copy()
        user = request.user
        
        # Set creator
        data['created_by'] = str(user.id)
        
        # Add creator to members if not already included
        if 'members' not in data:
            data['members'] = []
        
        if str(user.id) not in data['members']:
            data['members'].append(str(user.id))
        
        serializer = ChatRoomSerializer(data=data)
        if serializer.is_valid():
            room = serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def chat_room_detail(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "Chat room not found"}, status=404)
    
    # Check if user is a member
    user = request.user
    if user.id not in [str(member.id) for member in room.members]:
        return Response({"error": "You are not a member of this chat room"}, status=403)
    
    if request.method == 'GET':
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Only allow created_by to update room
        if str(room.created_by.id) != str(user.id):
            return Response({"error": "Only the room creator can update room details"}, status=403)
        
        data = request.data.copy()
        
        # Ensure we don't lose members
        if 'members' not in data:
            data['members'] = [str(member.id) for member in room.members]
        
        serializer = ChatRoomSerializer(room, data=data, partial=True)
        if serializer.is_valid():
            room = serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        # Only allow created_by to delete room
        if str(room.created_by.id) != str(user.id):
            return Response({"error": "Only the room creator can delete the room"}, status=403)
        
        room.delete()
        return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_chat_room(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "Chat room not found"}, status=404)
    
    user = request.user
    
    # Check if already a member
    if user.id in [str(member.id) for member in room.members]:
        return Response({"message": "Already a member of this chat room"})
    
    # Add user to members
    room.members.append(user)
    room.save()
    
    return Response({"message": "Successfully joined the chat room"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_chat_room(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "Chat room not found"}, status=404)
    
    user = request.user
    
    # Check if a member
    if user.id not in [str(member.id) for member in room.members]:
        return Response({"error": "Not a member of this chat room"}, status=400)
    
    # Cannot leave if creator
    if str(room.created_by.id) == str(user.id):
        return Response({"error": "Room creator cannot leave; delete the room instead"}, status=400)
    
    # Remove from members
    room.members = [member for member in room.members if str(member.id) != str(user.id)]
    room.save()
    
    return Response({"message": "Successfully left the chat room"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_messages(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({"error": "Chat room not found"}, status=404)
    
    # Check if user is a member
    user = request.user
    if user.id not in [str(member.id) for member in room.members]:
        return Response({"error": "You are not a member of this chat room"}, status=403)
    
    # Get messages, optionally with pagination
    limit = int(request.GET.get('limit', 50))
    offset = int(request.GET.get('offset', 0))
    
    messages = Message.objects.filter(room=room).order_by('-created_at')[offset:offset+limit]
    serializer = MessageSerializer(messages, many=True)
    
    return Response(serializer.data)