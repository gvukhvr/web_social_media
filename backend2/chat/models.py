from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_user1'
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_user2'
    )

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"


class Message(models.Model):
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']  # Сортировка по времени по умолчанию

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"