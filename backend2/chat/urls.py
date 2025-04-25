from django.urls import path
from .views import UserListView, PrivateChatRoomView, MessageListView, ChatRoomListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('chatroom/', PrivateChatRoomView.as_view(), name='chatroom'),
    path('messages/<int:room_id>/', MessageListView.as_view(), name='message-list'),
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
]
