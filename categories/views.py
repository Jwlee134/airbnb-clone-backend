from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

# Create your views here.

# GET, POST /categories
@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        # ORM을 통해 가져온 querySet을 CategorySerializer class에 정의된대로 JSON으로 변환
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # 사용자가 보낸 JSON을 CategorySerializer class에 정의된대로 querySet으로 변환
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"created": True})
        else:
            return Response(serializer.errors)


# GET /category/1
@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
