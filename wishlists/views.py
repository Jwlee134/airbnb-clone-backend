from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            wishlists, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        wishlist = serializer.save(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
