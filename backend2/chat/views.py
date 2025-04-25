from rest_framework import generics, permissions, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from django.contrib.auth import get_user_model
from .models import PrivateChatRoom, Message
from .serializers import UserSerializer, MessageSerializer, PrivateChatRoomSerializer, ChatRoomSerializer
from django.db.models import Q
from rest_framework import generics, permissions, filters

User = get_user_model()

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter] 
    search_fields = ['username']  

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)

class PrivateChatRoomView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user1 = request.user
        user2_id = request.data.get('user_id')
        if not user2_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        chat = PrivateChatRoom.objects.filter(
            Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
        ).first()

        if not chat:
            chat = PrivateChatRoom.objects.create(user1=user1, user2=user2)

        serializer = PrivateChatRoomSerializer(chat)
        return Response(serializer.data)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room_id=room_id).order_by('timestamp')
    
class ChatRoomListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rooms = PrivateChatRoom.objects.filter(user1=request.user) | PrivateChatRoom.objects.filter(user2=request.user)
        serializer = ChatRoomSerializer(rooms, many=True, context={'request': request})
        return Response(serializer.data)
