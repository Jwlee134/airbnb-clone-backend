from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class RoomCategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(kind=Category.CategoryKindChoices.ROOMS)


class ExperienceCategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(kind=Category.CategoryKindChoices.EXPERIENCES)
