from django.contrib import admin
from rooms.models import Room, Amenity

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "kind", "owner", "created", "updated")
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created",
        "updated",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created", "updated")
    readonly_fields = ("created", "updated")
