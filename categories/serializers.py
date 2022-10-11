from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fleid = "__all__" or ("name", "kind",) => 전부 보여줌 or 특정 필드
        exclude = ("updated",)  # => 특정 필드 제외 전부
