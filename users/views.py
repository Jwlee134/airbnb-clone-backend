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
import jwt
from django.conf import settings
import requests


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
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data="Wrong username or password."
            )
        login(request, user=user)  # Persist a user id and a backend in the request.
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUp(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        name = request.data.get("name")
        email = request.data.get("email")
        if not username or not password or not name or not email:
            raise exceptions.ParseError
        if User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_409_CONFLICT, data="This email is already in use."
            )
        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_409_CONFLICT, data="This username is already in use."
            )
        user = User.objects.create(name=name, username=username, email=email)
        user.set_password(password)
        user.save()
        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError
        # If the given credentials are valid, return a User object.
        user = authenticate(request, username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed("Wrong username or password.")
        token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
        return Response({"token": token})


class GithubLogin(APIView):
    def post(self, request):
        code = request.data.get("code")
        access_token = (
            requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id={settings.GH_CLIENT_ID}&client_secret={settings.GH_CLIENT_SECRET}",
                headers={"Accept": "application/json"},
            )
            .json()
            .get("access_token")
        )
        user_data = requests.get(
            "https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).json()
        emails = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        ).json()

        user, created = User.objects.get_or_create(
            email=emails[0]["email"],
            defaults={
                "username": user_data.get("login"),
                "name": user_data.get("name"),
                "avatar": user_data.get("avatar_url"),
            },
        )
        if created:
            user.set_unusable_password()
            user.save()
        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class KakaoLogin(APIView):
    def post(self, request):
        code = request.data.get("code")
        access_token = (
            requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KK_CLIENT_ID,
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            .json()
            .get("access_token")
        )
        user_data = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        ).json()
        kakao_account = user_data.get("kakao_account")
        profile = kakao_account.get("profile")
        user, created = User.objects.get_or_create(
            email=kakao_account.get("email"),
            defaults={
                "username": profile.get("nickname"),
                "name": profile.get("nickname"),
                "avatar": profile.get("thumbnail_image_url"),
            },
        )
        if created:
            user.set_unusable_password()
            user.save()
        login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)
