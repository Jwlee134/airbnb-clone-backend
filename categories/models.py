from django.db import models
from common.models import Common

# Create your models here.
class Category(Common):

    """Room or Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.kind.title()}: {self.name}"

    class Meta:
        # Admin panel에서 보여지는 클래스 이름 변경
        verbose_name_plural = "Categories"
