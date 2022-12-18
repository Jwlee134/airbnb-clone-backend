from rest_framework.views import APIView
from django.db import transaction
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitiySerializer, RoomDetailSerializer, RoomListSerializer
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from reviews.serializers import ReviewSerializer
from django.conf import settings
from media.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from django.utils import timezone


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomListSerializer(rooms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        category_pk = request.data.get("category")
        if not category_pk:
            raise ParseError("Category is required.")  # 400
        try:
            category = Category.objects.get(pk=category_pk)
            if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                raise ParseError("The type of category should be Rooms.")
        except Category.DoesNotExist:
            raise ParseError("Category does not exist.")
        try:
            with transaction.atomic():
                room = serializer.save(owner=request.user, category=category)
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    room.amenities.add(amenity)
                return Response(RoomDetailSerializer(room).data)
        except Exception:
            raise ParseError("Amenity does not exist.")


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        category_pk = request.data.get("category")
        category = room.category
        if category_pk:
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The type of category should be Rooms.")
            except Category.DoesNotExist:
                raise ParseError("Category does not exist.")
        try:
            with transaction.atomic():
                if category_pk:
                    room = serializer.save(category=category)
                else:
                    room = serializer.save()
                amenities = request.data.get("amenities")
                if amenities:
                    room.amenities.clear()
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                return Response(RoomDetailSerializer(room).data)
        except Exception:
            raise ParseError("Amenity does not exist.")

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitiySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitiySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitiySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = AmenitiySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = AmenitiySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitiySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        room = self.get_object(pk)
        limit = settings.LIMIT
        serializer = ReviewSerializer(
            room.reviews.all()[limit * page - limit : limit * page], many=True
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        review = serializer.save(
            user=request.user,
            room=self.get_object(pk),
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        room = self.get_object(pk)
        limit = settings.LIMIT
        serializer = AmenitiySerializer(
            room.amenities.all()[limit * page - limit : limit * page], many=True
        )
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerizalizer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_out__gte=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data, context={"room": room}
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        booking = serializer.save(
            room=room,
            user=request.user,
            kind=Booking.BookingKindChoices.ROOM,
        )
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)
