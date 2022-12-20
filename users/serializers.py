from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "avatar", "username")


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    total_rooms = SerializerMethodField()

    def get_total_rooms(self, user):
        return user.rooms.count()

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
