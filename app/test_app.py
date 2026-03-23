from unittest.mock import MagicMock


class MockService:
    def __init__(self, name, response):
        self.__setattr__(name, MagicMock(return_value=response))


class MockClient:
    service = None

    def __init__(self, name, response) -> None:
        service = MockService(name, response)
        self.service = service
