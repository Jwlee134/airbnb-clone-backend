from rest_framework.views import APIView
from .models import Perk
from .serializers import PerkSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


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
            raise NotFound

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
        return Response(status=HTTP_204_NO_CONTENT)
