from rest_framework.serializers import ModelSerializer
from .models import Amenity


class AmenitiySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"
