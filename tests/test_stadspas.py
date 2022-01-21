import os
from datetime import datetime
from unittest import TestCase

from hiro import Timeline
from mock import patch

from .mocks import MockClient

os.environ["FOCUS_USERNAME"] = "FOCUS_USERNAME"
os.environ["FOCUS_PASSWORD"] = "FOCUS_PASSWORD"
os.environ["FOCUS_WSDL"] = "focus/focus.wsdl"
os.environ["TMA_CERTIFICATE"] = __file__

from app.config import (
    config,
    credentials,
)  # noqa: E402  Module level import not at top of file
from app.focusconnect import FocusConnection  # noqa: E402


@Timeline(start=datetime(2017, 5, 1, 1, 1, 1))
@patch("focus.focusconnect.Client", new=MockClient)
class StadspasTest(TestCase):
    def test_get(self):
        focus_connection = FocusConnection(config, credentials)
        result = focus_connection.stadspas(bsn="1234")
        self.assertEqual(result, "8800000002")
