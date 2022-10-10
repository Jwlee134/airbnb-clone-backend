from rest_framework import serializers

from categories.models import Category

""" 
    required, max_length 같은 키워드 인자들을 정의해 주면
    post request 등의 데이터로 넘어온 필드들이 유효한지 검사할 수 있다.

    read_only 파라미터는 유저는 post request를 보낼 때 이 필드는
    데이터로 담을 수 없음을 의미한다.
"""


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created = serializers.DateTimeField(read_only=True)

    """ 
        **연산자
        딕셔너리 {"name": "Test", "kind": "rooms"} 를
        키워드 파라미터 형식 name="Test", kind="rooms" 으로 바꿔준다.
     """

    # 두 번째 인자로 위에 정의해놓은 키워드 인자들의 validation을 통과한 데이터가 들어온다.
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    # 두 번째 인자로 DB에서 가져온 원래 데이터가 들어온다.
    def update(self, instance, validated_data):
        """
        원래 데이터의 필드는 새로 들어오는 검증된 데이터의 필드가 있으면 그것으로 교체하고
        없으면 원래 데이터 필드의 값을 준다. (get은 첫 번째 인자의 이름을 가진 필드를 찾으면
        그것을 반환하고 없으면 두 번째 인자(default)를 반환한다.)
        """
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
