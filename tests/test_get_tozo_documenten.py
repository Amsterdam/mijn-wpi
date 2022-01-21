import os.path
from unittest import TestCase

# Prepare environment
from mock import patch

from tests.mocks import MockClient, MockClientEmpties

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
class TozoDocumentenTests(TestCase):
    def test_connection(self):
        self.maxDiff = None
        focus_connection = FocusConnection(zeep_config, focus_credentials)
        result = focus_connection.EAanvragenTozo(bsn=1234, url_root="/")
        expected = [
            {
                "datePublished": "2020-03-31T18:59:46+02:00",
                "description": "Tegemoetkoming Ondernemers en Zelfstandigen",
                "id": "4400000031",
                "documentCodeId": "770",
                "type": "E-AANVR-TOZO",
                "url": "/focus/document?id=4400000031&isBulk=true&isDms=false",
            },
            {
                "datePublished": "2020-03-26T15:18:44+01:00",
                "description": "Verkorte Aanvraag BBZ",
                "id": "4400000024",
                "documentCodeId": "756",
                "type": "E-AANVR-KBBZ",
                "url": "/focus/document?id=4400000024&isBulk=true&isDms=false",
            },
            {
                "datePublished": "2020-03-18T23:09:58+01:00",
                "description": "Ondernemerscheck zelfstandigen",
                "id": "4400000020",
                "documentCodeId": "734",
                "type": "E-AANVR-DGB",
                "url": "/focus/document?id=4400000020&isBulk=true&isDms=false",
            },
            {
                "datePublished": "2020-03-31T00:21:51+02:00",
                "description": "Tegemoetkoming Ondernemers en Zelfstandigen",
                "id": "4400000030",
                "documentCodeId": "770",
                "type": "E-AANVR-TOZO",
                "url": "/focus/document?id=4400000030&isBulk=true&isDms=false",
            },
            {
                "datePublished": "2020-03-22T00:26:10+01:00",
                "description": "Aanvraag BBZ",
                "id": "4400000022",
                "documentCodeId": "678",
                "type": "E-AANVR-BBZ",
                "url": "/focus/document?id=4400000022&isBulk=true&isDms=false",
            },
            {
                "datePublished": "2020-03-31T00:04:34+02:00",
                "description": "Tegemoetkoming Ondernemers en Zelfstandigen",
                "id": "4400000029",
                "documentCodeId": "770",
                "type": "E-AANVR-TOZO",
                "url": "/focus/document?id=4400000029&isBulk=true&isDms=false",
            },
        ]

        self.assertEqual(result, expected)


@patch("app.focusconnect.Client", new=MockClientEmpties)
class TozoDocumentenEmptyTests(TestCase):
    def test_connection(self):
        self.maxDiff = None
        focus_connection = FocusConnection(zeep_config, focus_credentials)
        result = focus_connection.EAanvragenTozo(bsn=1234, url_root="/")

        self.assertEqual(result, [])
