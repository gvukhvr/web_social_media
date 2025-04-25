import json
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message, PrivateChatRoom

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("[WEBSOCKET RECEIVE] RAW DATA:", data)

        message = data.get('message', '')
        sender = self.scope.get('user', None)

        if not message or sender is None:
            print("[WARNING] Missing message or sender.")
            return

        if not sender.is_authenticated:
            print("[WARNING] Anonymous user tried to send a message.")
            return

        room = await self.get_room(self.room_id)
        if not room:
            print(f"[ERROR] Chat room with id {self.room_id} not found.")
            return

        # Save message
        await self.save_message(room, sender, message)

        # Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': datetime.datetime.utcnow().isoformat() + "Z"
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'text': event.get('message', ''),  # Переименовано
            'sender': event.get('sender', 'anonymous'),
            'timestamp': event.get('timestamp', datetime.datetime.utcnow().isoformat() + "Z"),
        }))

    @database_sync_to_async
    def get_room(self, room_id):
        try:
            return PrivateChatRoom.objects.get(id=room_id)
        except PrivateChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, room, sender, text):
        return Message.objects.create(room=room, sender=sender, text=text)