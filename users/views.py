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
            user=request.user,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = serializer.save()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)
