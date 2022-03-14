from unittest.mock import MagicMock

from tma_saml import FlaskServerTMATestCase

from app.server import application


class WpiApiTestApp(FlaskServerTMATestCase):
    def setUp(self):
        self.client = self.get_tma_test_app(application)
        self.maxDiff = None

    TEST_BSN = "111222333"

    def get_secure(self, location):
        return self.client.get(location, headers=self.saml_headers())

    def saml_headers(self):
        return self.add_digi_d_headers(self.TEST_BSN)


class MockResponse:
    def __init__(self, reply, status_code=200):
        self.reply = reply
        self.status_code = status_code

    @property
    def content(self):
        return self.reply

    @property
    def data(self):
        return self.reply

    def json(self):
        return self.data

    def raise_for_status(self):
        return


class MockService:
    def __init__(self, name, response):
        self.__setattr__(name, MagicMock(return_value=response))


class MockClient:
    service = None

    def __init__(self, name, response) -> None:
        service = MockService(name, response)
        self.service = service
