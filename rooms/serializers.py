from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitiySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "price")


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer()
    amenities = AmenitiySerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Room
        fields = "__all__"