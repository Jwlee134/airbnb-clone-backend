from rest_framework.views import APIView
from .models import Perk, Experience
from bookings.models import Booking
from bookings.serializers import ExperienceBookingSerializer
from categories.models import Category
from .serializers import (
    PerkSerializer,
    ExperienceSerializer,
    ExperienceDetailSerializer,
)
from bookings.serializers import CreateExperienceBookingSerializer
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from common.paginations import PagePagination
from django.db import transaction


class Perks(APIView):
    def get(self, request):
        perks = Perk.objects.all()
        serializer = PerkSerializer(perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        serializer = PerkSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = PerkSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk=pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Experiences(APIView, PagePagination):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(
            self.paginate(request, experiences), many=True
        )
        return Response(self.response(serializer.data, experiences.count()))

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        category_pk = request.data.get("category")
        if not category_pk:
            raise exceptions.ParseError("Category is required.")
        try:
            category = Category.objects.get(pk=category_pk)
            if category.kind == Category.CategoryKindChoices.ROOMS:
                raise exceptions.ParseError("The type of category should not be rooms.")
        except Category.DoesNotExist:
            raise exceptions.ParseError("Category doesn't exist.")
        try:
            with transaction.atomic():
                experience = serializer.save(host=request.user, category=category)
                perks = request.data.get("perks")
                for perk_pk in perks:
                    perk = Perk.objects.get(pk=perk_pk)
                    experience.perks.add(perk)
                return Response({"pk": experience.pk})
        except:
            raise exceptions.ParseError("Perks don't exist.")


class ExperiencePerks(APIView, PagePagination):
    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        perks = experience.perks.all()
        serializer = PerkSerializer(self.paginate(request, perks), many=True)
        return Response(self.response(serializer.data, perks.count()))


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        serializer = ExperienceDetailSerializer(
            experience, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        category_pk = request.data.get("category")
        category = experience.category
        if category_pk:
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise exceptions.ParseError("Category kind should be experiences.")
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category doesn't exist.")
        try:
            with transaction.atomic():
                if category_pk:
                    experience = serializer.save(category=category)
                else:
                    experience = serializer.save()
                perks = request.data.get("perks")
                if perks:
                    experience.perks.clear()
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            raise exceptions.ParseError("Perk doesn't exist.")

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceBookings(APIView):
    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data, context={"experience": experience}
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save(
            kind=Booking.BookingKindChoices.EXPERIENCE,
            user=request.user,
            experience=experience,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceBooking(APIView):
    permission_classes = [IsAuthenticated]

    def get_experience(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
            return experience
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get_object(self, pk):
        try:
            booking = Booking.objects.get(
                pk=pk, kind=Booking.BookingKindChoices.EXPERIENCE
            )
            return booking
        except Booking.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk, booking_pk):
        booking = self.get_object(booking_pk)
        serializer = ExperienceBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        experience = self.get_experience(pk)
        booking = self.get_object(booking_pk)
        serializer = CreateExperienceBookingSerializer(
            booking, data=request.data, context={"experience": experience}, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk, booking_pk):
        booking = self.get_object(booking_pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
