from rest_framework.serializers import (
    ModelSerializer,
    DateField,
    ValidationError,
    DateTimeField,
)
from .models import Booking
from django.utils import timezone
from datetime import datetime


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
        fields = ("id", "check_in", "check_out")


class CreateExperienceBookingSerializer(ModelSerializer):
    experience_time = DateTimeField()

    class Meta:
        model = Booking
        fields = ("experience_time", "guests")

    def validate_guests(self, value):
        # 예약 인원 수가 max guests보다 많으면 invalid
        max_guests = self.context["experience"].max_guests
        if max_guests < value:
            raise ValidationError("Too many guests.")

        return value

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        start = self.context["experience"].start
        """ 
            이벤트 시간이 6am-6pm 이라고 가정
            value로는 날짜와 이벤트의 시작 시간이 들어온다.
            날짜를 포함한 이벤트 시작 시간이 value보다 작으면 이벤트가 이미 시작했다는 뜻이다.
            ex) 2022-12-25 6am(start) <= 2022-12-25 6am(value) ? 이벤트 이미 시작함

            experience model의 start는 TimeField이므로 여기에 현재 날짜를 결합해야 한다.
            => datetime.combine(timezone.localtime(timezone.now()).date(), start)

            프론트에서 보내는 ISOString은 kst 시간대를 포함한 aware datetime으로 자동으로 변환되므로 신경쓸 필요가 없다.

            그런데 datetime.combine은 시간대를 포함하지 않은 naive datetime이 반환된다. 따라서
            timezone.make_aware를 사용하여 aware datetime으로 변환하는데 default는 utc이므로
            timezone.localtime으로 다시 kst로 변환해준다.
         """
        event_time = timezone.localtime(
            timezone.make_aware(
                datetime.combine(timezone.localtime(timezone.now()).date(), start),
            )
        )
        if now > value:
            raise ValidationError("Can't book in the past.")
        return value

    def validate(self, data):
        # bookings의 guests를 모두 더한 수가 experience의 max guests보다 많으면 invalid
        experience = self.context["experience"]
        requested_time = data["experience_time"]
        guests = data["guests"]
        bookings = Booking.objects.filter(
            experience=experience, experience_time=requested_time
        )
        count = 0
        for booking in bookings:
            count = count + booking.guests
        if count + guests > experience.max_guests:
            raise ValidationError("Too much guests.")
        return data
