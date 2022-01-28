import os.path
from unittest import TestCase

# Prepare environment
from mock import patch

from tests.mocks import MockClient

os.environ["FOCUS_USERNAME"] = "FOCUS_USERNAME"
os.environ["FOCUS_PASSWORD"] = "FOCUS_PASSWORD"
os.environ["FOCUS_WSDL"] = "focus/focus.wsdl"
os.environ["TMA_CERTIFICATE"] = __file__

from app.config import (
    zeep_config,
    focus_credentials,
)  # noqa: E402  Module level import not at top of file
from app.old.focusconnect import FocusConnection  # noqa: E402


@patch("app.focusconnect.Client", new=MockClient)
class UitkeringsspecificatiesTests(TestCase):
    def test_connection(self):
        focus_connection = FocusConnection(zeep_config, focus_credentials)
        result = focus_connection.uitkeringsspecificaties(bsn=1234, url_root="/")

        expected = [
            {
                "title": "Uitkeringsspecificatie",
                "datePublished": "2019-04-19T00:00:00+02:00",
                "id": "24233351",
                "url": "/focus/document?id=24233351&isBulk=false&isDms=false",
                "type": "Participatiewet",
            },
            {
                "title": "Uitkeringsspecificatie",
                "datePublished": "2014-01-24T00:00:00+01:00",
                "id": "30364921",
                "url": "/focus/document?id=30364921&isBulk=false&isDms=false",
                "type": "",
            },
        ]

        self.assertEqual(result, expected)
