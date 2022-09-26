from django.contrib import admin
from rooms.models import Room, Amenity

# Register your models here.


# admin 패널 액션 선언
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating_average",
        "owner",
        "created",
        "updated",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created",
        "updated",
        "category",
    )
    search_fields = (
        "=owner__username",  # foreign key
        # "^name",  # startswith
        # "=price",  # exact
    )
    # 액션 실제로 추가
    actions = (reset_prices,)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created", "updated")
    readonly_fields = ("created", "updated")
