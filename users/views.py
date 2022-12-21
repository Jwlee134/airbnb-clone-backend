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
from django.contrib.auth import authenticate, login, logout
from common.paginations import PagePagination


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


class PublicUserRooms(APIView, PagePagination):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
        rooms = Room.objects.filter(owner=user)
        serializer = RoomListSerializer(
            self.paginate(request, rooms),
            many=True,
            context={"request": request},
        )
        return Response(self.response(serializer.data, rooms.count()))


class PublicUserReviews(APIView, PagePagination):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
        reviews = Review.objects.filter(user=user)
        serializer = ReviewListSerializer(
            self.paginate(request, reviews),
            many=True,
        )
        return Response(self.response(serializer.data, reviews.count()))


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


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError
        # If the given credentials are valid, return a User object.
        user = authenticate(request, username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed("Wrong username or password.")
        login(request, user=user)  # Persist a user id and a backend in the request.
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
