from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from wishlists.models import Wishlist
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from rest_framework.serializers import SerializerMethodField
from media.serializers import PhotoSerializer


class AmenitiySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")


class RoomListSerializer(ModelSerializer):
    rating_average = SerializerMethodField()
    is_owner = SerializerMethodField()

    photos = PhotoSerializer(read_only=True, many=True)

    def get_rating_average(self, room):
        return room.rating_average()

    def get_is_owner(self, room):
        request = self.context["request"]
        return request.user == room.owner

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "is_owner",
            "rating_average",
            "photos",
        )


class ReviewListRoomSerializer(ModelSerializer):
    thumbnail = SerializerMethodField()

    def get_thumbnail(self, room):
        return room.photos.all()[0].file

    class Meta:
        model = Room
        fields = ("pk", "name", "thumbnail")


class RoomDetailSerializer(ModelSerializer):
    """
    read_only=True => put, delete 요청 등에서 해당 필드를 넣지 않아도
    request.data가 valid하게 됨 => 원래 있던 데이터가 들어감
    """

    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    rating_average = SerializerMethodField()
    is_owner = SerializerMethodField()
    is_liked = SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    def get_rating_average(self, room):
        return room.rating_average()

    def get_is_owner(self, room):
        request = self.context["request"]
        return request.user == room.owner

    def get_is_liked(self, room):
        request = self.context["request"]
        if Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists():
            return True
        return False

    class Meta:
        model = Room
        fields = "__all__"


""" 
TODO: RoomDetailSerializer에서 get 메소드일때만 amenities exclude하기
 """
