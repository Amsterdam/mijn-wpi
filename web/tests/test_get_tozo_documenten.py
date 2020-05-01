import os.path
from unittest import TestCase

# Prepare environment
from mock import patch

from tests.mocks import MockClient

os.environ['FOCUS_USERNAME'] = 'FOCUS_USERNAME'
os.environ['FOCUS_PASSWORD'] = 'FOCUS_PASSWORD'
os.environ['FOCUS_WSDL'] = 'focus/focus.wsdl'
os.environ['TMA_CERTIFICATE'] = __file__

from focus.config import config, credentials  # noqa: E402  Module level import not at top of file
from focus.focusconnect import FocusConnection  # noqa: E402


@patch('focus.focusconnect.Client', new=MockClient)
class TozoDocumentenTests(TestCase):
    def test_connection(self):
        self.maxDiff = None
        focus_connection = FocusConnection(config, credentials)
        result = focus_connection.EAanvragenTozo(bsn=1234, url_root='/')
        expected = [
            {
                'datePublished': '2020-03-31T18:59:46+02:00',
                'description': 'Tegemoetkoming Ondernemers en Zelfstandigen',
                'id': '4400000031',
                'type': 'E-AANVR-TOZO',
                'url': '/focus/document?id=4400000031&isBulk=true&isDms=false'
            },
            {
                'datePublished': '2020-03-26T15:18:44+01:00',
                'description': 'Verkorte Aanvraag BBZ',
                'id': '4400000024',
                'type': 'E-AANVR-KBBZ',
                'url': '/focus/document?id=4400000024&isBulk=true&isDms=false'
            },
            {
                'datePublished': '2020-03-18T23:09:58+01:00',
                'description': 'Ondernemerscheck zelfstandigen',
                'id': '4400000020',
                'type': 'E-AANVR-DGB',
                'url': '/focus/document?id=4400000020&isBulk=true&isDms=false'
            },
            {
                'datePublished': '2020-03-31T00:21:51+02:00',
                'description': 'Tegemoetkoming Ondernemers en Zelfstandigen',
                'id': '4400000030',
                'type': 'E-AANVR-TOZO',
                'url': '/focus/document?id=4400000030&isBulk=true&isDms=false'
            },
            {
                'datePublished': '2020-03-22T00:26:10+01:00',
                'description': 'Aanvraag BBZ',
                'id': '4400000022',
                'type': 'E-AANVR-BBZ',
                'url': '/focus/document?id=4400000022&isBulk=true&isDms=false'
            },
            {
                'datePublished': '2020-03-31T00:04:34+02:00',
                'description': 'Tegemoetkoming Ondernemers en Zelfstandigen',
                'id': '4400000029',
                'type': 'E-AANVR-TOZO',
                'url': '/focus/document?id=4400000029&isBulk=true&isDms=false'
            }
        ]

        self.assertEqual(result, expected)
