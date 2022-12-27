from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Description"

    # 테스트가 실행되기 전 해야 할 일
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_all_amenities(self):
        res = self.client.get("/api/v1/rooms/amenities/")  # 테스트할 url로 요청
        data = res.json()  # json 데이터
        self.assertEqual(res.status_code, 200)  # status code가 200인가?
        self.assertIsInstance(data, list)  # 데이터가 list인가?
        self.assertEqual(len(data), 1)  # setUp에서 하나만 생성했으니 길이가 1인가?
        self.assertEqual(data[0]["name"], self.NAME)  # 생성한 데이터의 이름이 일치하는가?
        self.assertEqual(data[0]["description"], self.DESC)  # 생성한 설명의 이름이 일치하는가?
