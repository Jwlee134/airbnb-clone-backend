from django.db import models
from common.models import Common

# Create your models here.


class Chatroom(Common):

    """Chatroom Model Definition"""

    users = models.ManyToManyField("users.User")

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
    )
    room = models.ForeignKey(
        "direct_messages.Chatroom",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.user}: {self.text}"
