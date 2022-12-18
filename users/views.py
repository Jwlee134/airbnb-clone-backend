from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from .serializers import PrivateUserSerializer


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
