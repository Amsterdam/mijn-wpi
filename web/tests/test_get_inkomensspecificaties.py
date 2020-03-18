import os.path
from unittest import TestCase

# Prepare environment
from flask_testing import TestCase as FlaskTestCase
from mock import patch

from web.tests.mocks import MockClient

os.environ['FOCUS_USERNAME'] = 'FOCUS_USERNAME'
os.environ['FOCUS_PASSWORD'] = 'FOCUS_PASSWORD'
os.environ['FOCUS_WSDL'] = 'focus/focus.wsdl'
os.environ['TMA_CERTIFICATE'] = __file__

from focus.config import BASE_PATH, config, credentials  # noqa: E402  Module level import not at top of file
from focus.focusconnect import FocusConnection  # noqa: E402
from focus.server import application  # noqa: E402


@patch('focus.focusconnect.Client', new=MockClient)
class UitkeringspecificatiesTests(TestCase):
    def test_connection(self):
        focus_connection = FocusConnection(config, credentials)
        result = focus_connection.uitkeringspecificaties(bsn=1234, url_root='/')

        expected = [
            {
                'title': 'Uitkeringsspecificatie',
                'datePublished': '2019-04-19T00:00:00+02:00',
                'id': '172013',
                'url': '/?id=172013&isBulk=false&isDms=false',
                'type': '',
                'isAnnualStatement': False
            },
            {
                'title': 'Uitkeringsspecificatie',
                'datePublished': '2014-01-24T00:00:00+01:00',
                'id': '172013',
                'url': '/?id=172013&isBulk=false&isDms=false',
                'type': '',
                'isAnnualStatement': False
            }
        ]

        self.assertEqual(result, expected)
