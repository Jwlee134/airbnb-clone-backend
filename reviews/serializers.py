from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from rooms.serializers import ReviewListRoomSerializer
from .models import Review


class ReviewSerializer(ModelSerializer):
    """
    RoomReviews에서 review를 생성할 때 request.data(body)에 user가 없어도
    serializer가 유효하게 만들기 위해 read_only=True
    왜냐면 user는 백엔드에서 request.user를 통해 추가할 것이기 때문
    """

    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "payload", "rating")


class ReviewListSerializer(ModelSerializer):
    room = ReviewListRoomSerializer()

    class Meta:
        model = Review
        fields = ("pk", "room", "created", "payload", "rating")
