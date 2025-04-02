import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatRoom, Message
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Check if room exists and user is a member
        room_exists = await self.room_exists()
        if not room_exists:
            await self.close()
            return

        # Add user to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        # Send join message
        user_id = self.scope['user'].id if self.scope['user'].is_authenticated else None
        if user_id:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user_id': str(user_id)
                }
            )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Send leave message
        user_id = self.scope['user'].id if self.scope['user'].is_authenticated else None
        if user_id:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user_id': str(user_id)
                }
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        user_id = self.scope['user'].id
        
        # Save message to database
        msg = await self.save_message(message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': str(user_id),
                'message_id': str(msg.id),
                'timestamp': msg.created_at.isoformat()
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'user_id': event['user_id'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp']
        }))

    async def user_join(self, event):
        # Send user join notification
        user = await self.get_user(event['user_id'])
        if user:
            await self.send(text_data=json.dumps({
                'type': 'join',
                'user_id': event['user_id'],
                'username': f"{user.first_name} {user.last_name}"
            }))

    async def user_leave(self, event):
        # Send user leave notification
        user = await self.get_user(event['user_id'])
        if user:
            await self.send(text_data=json.dumps({
                'type': 'leave',
                'user_id': event['user_id'],
                'username': f"{user.first_name} {user.last_name}"
            }))

    @database_sync_to_async
    def room_exists(self):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            user = self.scope['user']
            
            # Check if anonymous or not in room members
            if not user.is_authenticated or user.id not in [str(member.id) for member in room.members]:
                return False
                
            return True
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        room = ChatRoom.objects.get(id=self.room_id)
        user = User.objects.get(id=self.scope['user'].id)
        message = Message(room=room, sender=user, content=content)
        message.save()
        return message

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
