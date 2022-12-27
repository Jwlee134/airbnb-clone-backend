from rest_framework.test import APITestCase
from django.utils.crypto import get_random_string
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
        self.assertEqual(data["name"], new_amenity_name, "Name doesn't match.")
        self.assertEqual(data["description"], new_amenity_desc, "Desc doesn't match.")

        res = self.client.post(self.URL)
        data = res.json()
        self.assertEqual(res.status_code, 400, "Status code isn't 400.")
        self.assertIn("name", data, "Name field doesn't exist.")


# 위 클래스의 테스트가 끝나면 DB는 초기화된다.


class TestAmenity(APITestCase):
    NAME = "Amenity Test"
    UPDATED_NAME = "Updated Amenity Test"
    DESC = "Amenity Description"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    # setUp에서 처음 하나를 생성했으니 id가 1인 amenity 하나만 있어야 한다. 그런데 2를 요청했으니 404가 떠야한다.
    def test_ammenity_not_found(self):
        res = self.client.get("/api/v1/rooms/amenities/2")
        self.assertEqual(res.status_code, 404, "Status code isn't 404.")

    def test_get_amenity(self):
        res = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(res.status_code, 200, "Status code isn't 200.")
        data = res.json()
        self.assertEqual(data["name"], self.NAME, "Name doesn't match.")
        self.assertEqual(data["description"], self.DESC, "Desc doesn't match.")

    def test_put_amenity(self):
        # name의 최대 length는 150인데 넘기면 400 에러가 반환되어야 한다.
        res = self.client.put(
            "/api/v1/rooms/amenities/1", data={"name": get_random_string(length=151)}
        )
        self.assertEqual(res.status_code, 400, "Status code isn't 400.")

        res = self.client.put(
            "/api/v1/rooms/amenities/1", data={"name": self.UPDATED_NAME}
        )
        self.assertEqual(res.status_code, 200, "Status code isn't 200.")
        data = res.json()
        self.assertEqual(data["name"], self.UPDATED_NAME, "Name doesn't match.")

    def test_delete_amenity(self):
        res = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(res.status_code, 204, "Status code isn't 204.")
