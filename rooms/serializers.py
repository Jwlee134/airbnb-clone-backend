from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from rest_framework.serializers import SerializerMethodField


class AmenitiySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")


class RoomListSerializer(ModelSerializer):
    rating_average = SerializerMethodField()

    def get_rating_average(self, room):
        return room.rating_average()

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "price", "rating_average")


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitiySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating_average = SerializerMethodField()

    def get_rating_average(self, room):
        return room.rating_average()

    class Meta:
        model = Room
        fields = "__all__"
