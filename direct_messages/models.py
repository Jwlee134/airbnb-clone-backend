from django.db import models
from common.models import Common

# Create your models here.


class Chatroom(Common):

    """Chatroom Model Definition"""

    users = models.ManyToManyField(
        "users.User",
        related_name="chatrooms",
    )

    def __str__(self) -> str:
        return "Chatroom"


class Message(Common):

    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    room = models.ForeignKey(
        "direct_messages.Chatroom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self) -> str:
        return f"{self.user}: {self.text}"
