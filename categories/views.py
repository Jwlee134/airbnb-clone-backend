from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class Categories(APIView):
    def get(self, request):
        categories = Category.objects.all()
        # ORM을 통해 가져온 querySet을 CategorySerializer class에 정의된대로 JSON으로 변환
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 사용자가 보낸 JSON을 CategorySerializer class에 정의된대로 querySet으로 변환
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # save 메소드는 내부적으로 CategorySerializer의 create 메소드를 호출한다.
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):
    # 각 메소드마다 공통으로 사용되는 객체를 리턴할 때 만드는 일종의 컨벤션 메소드
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,  # 특정 필드만 업데이트를 위해 필수 필드도 옵셔널하게 만들고 싶을 때
        )
        if serializer.is_valid():
            """
            DB에서 가져온 category와 들어오는 데이터(두 번째 키워드 인자)를 합쳐
            serialize한다는 것을 알기 때문에(업데이트) create가 아닌 update가 실행된다.
            """
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
