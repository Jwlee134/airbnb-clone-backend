from django.db import models

from common.models import Common

# Create your models here.
class Room(Common):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(
        max_length=180,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.TextField(
        max_length=200,
    )
    pet_friendly = models.BooleanField(
        default=True,
    )
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self):
        return self.name

    # Django ORM을 이용한 커스텀 필드 정의
    def total_amenities(self):
        return self.amenities.count()

    def rating_average(self):
        count = self.reviews.count()
        if count == 0:
            return "No Reviews"
        total = 0
        # 특정 필드만 select하는 방법
        for review in self.reviews.all().values("rating"):
            total += review["rating"]
        return round(total / count, 2)


class Amenity(Common):

    """Amenity Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        # Admin panel에서 보여지는 클래스 이름 변경
        verbose_name_plural = "Amenities"


""" 
    Many To One
    One To Many
    Many To Many

    [Room1, Room2, Room3] => User1  (Many To One)
    User1 => [Room1, Room2, Room3]  (One To Many)
    [Amenity1, Amenity2, Amenity3] => [Room1, Room2, Room3]  (Many To Many)
    여러 종류의 Amenities를 여러 Rooms가 동시에 가질 수 있다.
"""
