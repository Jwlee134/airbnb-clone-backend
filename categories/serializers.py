from rest_framework import serializers

""" 
    required, max_length 같은 파라미터를 정의해 주면
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
    kind = serializers.CharField(
        max_length=15,
    )
    created = serializers.DateTimeField(read_only=True)
