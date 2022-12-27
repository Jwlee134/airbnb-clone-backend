from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Description"
    URL = "/api/v1/rooms/amenities/"

    # 테스트가 실행되기 전 해야 할 일
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_all_amenities(self):
        res = self.client.get(self.URL)  # 테스트할 url로 요청
        data = res.json()  # json 데이터
        self.assertEqual(
            res.status_code, 200, "Status code isn't 200."
        )  # status code가 200인가?
        self.assertIsInstance(data, list, "Data isn't list.")  # 데이터가 list인가?
        self.assertEqual(len(data), 1)  # setUp에서 하나만 생성했으니 길이가 1인가?
        self.assertEqual(data[0]["name"], self.NAME)  # 생성한 데이터의 이름이 일치하는가?
        self.assertEqual(data[0]["description"], self.DESC)  # 생성한 설명의 이름이 일치하는가?

    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity desc"

        res = self.client.post(
            self.URL, data={"name": new_amenity_name, "description": new_amenity_desc}
        )
        data = res.json()
        self.assertEqual(res.status_code, 200, "Status code isn't 200.")
        self.assertEqual(data["name"], new_amenity_name, "Name isn't match.")
        self.assertEqual(data["description"], new_amenity_desc, "Desc isn't match.")

        res = self.client.post(self.URL)
        data = res.json()
        self.assertEqual(res.status_code, 400, "Status code isn't 400.")
        self.assertIn("name", data, "Name field doesn't exist.")
