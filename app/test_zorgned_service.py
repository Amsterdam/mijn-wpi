import json
from unittest import TestCase
from unittest.mock import patch
from app.config import BASE_PATH

from app.zorgned_service import get_clientnummer, volledig_clientnummer


class ZorgnedApiMock:
    status_code = 200
    response_json = None
    content = {"mock": "Data"}

    def __init__(self, response_json=None, status_code=200):
        self.status_code = status_code

        if isinstance(response_json, str):
            with open(response_json, "r") as read_file:
                self.response_json = json.load(read_file)
        else:
            self.response_json = response_json

    def json(self):
        return self.response_json

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("Request failed")


class ZorgnedServiceTest(TestCase):
    @patch("app.zorgned_service.requests.post")
    def test_get_clientnummer_response(self, get_mock):
        get_mock.return_value = ZorgnedApiMock(BASE_PATH + "/fixtures/persoon.json")

        clientnummer = get_clientnummer(123)

        self.assertEqual(clientnummer, 304184)

    @patch("app.zorgned_service.requests.post")
    def test_get_clientnummer_not_found_response(self, get_mock):
        get_mock.return_value = ZorgnedApiMock(status_code=404)

        clientnummer = get_clientnummer(123)

        self.assertEqual(clientnummer, None)

    @patch("app.zorgned_service.requests.post")
    def test_get_clientnummer_bad_request_response(self, get_mock):
        get_mock.return_value = ZorgnedApiMock(status_code=400)

        self.assertRaises(Exception, get_clientnummer, 123)

    def test_volledig_clientnummer(self):
        self.assertEqual(volledig_clientnummer(304184), "03630000304184")
