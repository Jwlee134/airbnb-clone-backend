from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
    created = serializers.DateTimeField()
