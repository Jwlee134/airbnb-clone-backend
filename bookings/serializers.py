from rest_framework.serializers import ModelSerializer, DateField, ValidationError
from .models import Booking
from django.utils import timezone


class CreateRoomBookingSerializer(ModelSerializer):
    # Booking 모델에서 아래 두 필드는 optional이므로 required한 필드로 덮어쓴다.
    # 덮어쓰지 않으면 프론트에서 check_in or out을 보내지 않아도 valid됨
    check_in = DateField()
    check_out = DateField()

    class Meta:
        model = Booking
        fields = ("check_in", "check_out", "guests")

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book in the past.")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise ValidationError("Can't book in the past.")
        return value


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out")
