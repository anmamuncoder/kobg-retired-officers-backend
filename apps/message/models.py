from django.db import models
from apps.base.models import BaseModel
from apps.user.models import User


class Message(BaseModel):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")

    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.sender}"


class MessageReply(BaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="replies")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_replies")
    body = models.TextField()

    def __str__(self):
        return f"Reply to {self.message.id} by {self.sender}"

