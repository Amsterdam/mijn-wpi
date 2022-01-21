import os.path
from unittest import TestCase

# Prepare environment
from mock import patch

from .mocks import MockClient

os.environ["FOCUS_USERNAME"] = "FOCUS_USERNAME"
os.environ["FOCUS_PASSWORD"] = "FOCUS_PASSWORD"
os.environ["FOCUS_WSDL"] = "focus/focus.wsdl"
os.environ["TMA_CERTIFICATE"] = __file__

from app.config import (
    zeep_config,
    focus_credentials,
)  # noqa: E402  Module level import not at top of file
from app.focusconnect import FocusConnection  # noqa: E402


@patch("app.focusconnect.Client", new=MockClient)
class JaaropgavenTest(TestCase):
    def test_connection(self):
        focus_connection = FocusConnection(zeep_config, focus_credentials)
        result = focus_connection.jaaropgaven(bsn=1234, url_root="/")
        expected = [
            {
                "datePublished": "2011-01-28T00:00:00+01:00",
                "id": "95330222",
                "title": "Jaaropgave",
                "type": "",
                "url": "/focus/document?id=95330222&isBulk=false&isDms=false",
            },
            {
                "datePublished": "2019-01-04T00:00:00+01:00",
                "id": "20021871",
                "title": "Jaaropgave",
                "type": "",
                "url": "/focus/document?id=20021871&isBulk=false&isDms=false",
            },
        ]

        self.assertEqual(result, expected)