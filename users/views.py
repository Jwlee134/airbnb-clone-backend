from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from .serializers import PrivateUserSerializer, PublicUserSerializer
from rooms.serializers import RoomListSerializer
from reviews.serializers import ReviewListSerializer
from users.models import User
from rooms.models import Room
from reviews.models import Review
from django.conf import settings
import math


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PrivateUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = PrivateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        """ 
            ModelSerializer는 unique field validation을 자동으로 해주기 때문에
            email이나 username 같은 것들의 validation을 진행할 필요가 없다.
         """
        user = serializer.save()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise exceptions.ParseError("Password is required.")
        serializer = PrivateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = serializer.save()
        # password를 암호화하여 저장한다.
        user.set_password(password)
        user.save()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class PublicUserRooms(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        limit = settings.LIMIT
        total_page = math.ceil(Room.objects.filter(owner=user).count() / limit)
        rooms = RoomListSerializer(
            Room.objects.filter(owner=user)[page * limit - limit : page * limit],
            many=True,
            context={"request": request},
        )
        return Response({"total_page": total_page, "data": rooms.data})


class PublicUserReviews(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        limit = settings.LIMIT
        total_page = math.ceil(Review.objects.filter(user=user).count() / limit)
        reviews = ReviewListSerializer(
            Review.objects.filter(user=user)[page * limit - limit : page * limit],
            many=True,
        )
        return Response({"total_page": total_page, "data": reviews.data})


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_pw = request.data.get("old_password")
        new_pw = request.data.get("new_password")
        if (not old_pw or not new_pw) or not user.check_password(old_pw):
            raise exceptions.ParseError
        user.set_password(new_pw)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
