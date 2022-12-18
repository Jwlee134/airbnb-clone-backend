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

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise ValidationError("Check in should be eariler than check out.")
        if Booking.objects.filter(
            room=self.context["room"],
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise ValidationError("There is an existing booking.")
        return data


class PublicBookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out")
