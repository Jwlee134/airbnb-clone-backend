from django.db import models
from common.models import Common

# Create your models here.


class Experience(Common):

    """Experience Model Definition"""

    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    name = models.CharField(max_length=200)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    # TimeField는 h, m, s만 저장한다.
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey(
        "categories.Category", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return self.name


class Perk(Common):

    """What is included on an experience"""

    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=250, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
