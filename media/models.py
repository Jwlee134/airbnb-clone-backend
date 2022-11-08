from django.db import models
from common.models import Common

# Create your models here.


class Photo(Common):
    file = models.URLField()
    description = models.CharField(max_length=140)
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(Common):
    file = models.URLField()
    # 하나의 experiences는 하나의 video만 가질 수 있다.
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="video",
    )

    def __str__(self) -> str:
        return "Video File"
