from rest_framework.views import APIView
from django.db import transaction
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitiySerializer, RoomDetailSerializer, RoomListSerializer
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT


class Rooms(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated
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
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        return Response(RoomDetailSerializer(room).data)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            raise NotAuthenticated
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
        if not request.user.is_authenticated:
            raise NotAuthenticated
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
