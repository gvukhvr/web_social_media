from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PrivateChatRoom, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    timestamp = serializers.DateTimeField()

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'text', 'timestamp']

class PrivateChatRoomSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = PrivateChatRoom
        fields = ['id', 'user1', 'user2', 'messages']

class ChatRoomSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChatRoom
        fields = ['id', 'other_user']

    def get_other_user(self, obj):
        request_user = self.context['request'].user
        return UserSerializer(obj.user2 if obj.user1 == request_user else obj.user1).data