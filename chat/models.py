from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, default='새 대화')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def get_messages_for_api(self):
        """OpenAI API 호출용 메시지 형식으로 변환"""
        messages = []
        for message in self.messages.filter(is_active=True):
            messages.append({
                "role": message.role,
                "content": message.content
            })
        return messages


class Message(models.Model):
    ROLE_CHOICES = [
        ('user', '사용자'),
        ('assistant', '어시스턴트'),
        ('system', '시스템'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.conversation.title} - {self.role}: {self.content[:50]}..."
