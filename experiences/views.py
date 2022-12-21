from rest_framework.views import APIView
from .models import Perk, Experience
from categories.models import Category
from .serializers import PerkSerializer, ExperienceSerializer
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
        category = Category.objects.get(pk=category_pk)
        if category.kind == Category.CategoryKindChoices.ROOMS:
            raise exceptions.ParseError("The type of category should not be rooms.")
        try:
            with transaction.atomic():
                experience = serializer.save(host=request.user, category=category)
                perks = request.data.get("perks")
                for perk_pk in perks:
                    perk = Perk.objects.get(pk=perk_pk)
                    experience.perks.add(perk)
        except:
            raise exceptions.ParseError("Perks don't exist.")
        return Response({"pk": experience.pk})


class ExperiencePerks(APIView, PagePagination):
    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound
        return experience

    def get(self, request, pk):
        experience = self.get_object(pk)
        perks = experience.perks.all()
        serializer = PerkSerializer(self.paginate(request, perks), many=True)
        return Response(self.response(serializer.data, perks.count()))


class ExperienceDetail(APIView):
    def get_object(self, pk):
        try:
            experience = Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound
        return experience

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class ExperienceBookings(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass
