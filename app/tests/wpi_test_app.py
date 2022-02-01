from unittest.mock import MagicMock, patch

from tma_saml import FlaskServerTMATestCase

from app.server import application


class WpiApiTestApp(FlaskServerTMATestCase):
    def setUp(self):
        self.client = self.get_tma_test_app(application)
        self.maxDiff = None


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


FERNET_KEY_MOCK = "z4QXWk3bjwFST2HRRVidnn7Se8VFCaHscK39JfODzNs="


class MockService:
    def __init__(self, name, response):
        self.__setattr__(name, MagicMock(return_value=response))


class MockClient:
    service = None

    def __init__(self, name, response) -> None:
        service = MockService(name, response)
        self.service = service
