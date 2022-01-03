import os.path
from unittest import TestCase

# Prepare environment
from mock import patch

from .mocks import MockClient

os.environ['FOCUS_USERNAME'] = 'FOCUS_USERNAME'
os.environ['FOCUS_PASSWORD'] = 'FOCUS_PASSWORD'
os.environ['FOCUS_WSDL'] = 'focus/focus.wsdl'
os.environ['TMA_CERTIFICATE'] = __file__

from focus.config import config, credentials  # noqa: E402  Module level import not at top of file
from focus.focusconnect import FocusConnection  # noqa: E402


@patch('focus.focusconnect.Client', new=MockClient)
class JaaropgavenTest(TestCase):
    def test_connection(self):
        focus_connection = FocusConnection(config, credentials)
        result = focus_connection.jaaropgaven(bsn=1234, url_root='/')
        expected = [
            {
                'datePublished': '2011-01-28T00:00:00+01:00',
                'id': '95330222',
                'title': 'Jaaropgave',
                'type': '',
                'url': '/focus/document?id=95330222&isBulk=false&isDms=false'
            },
            {
                'datePublished': '2019-01-04T00:00:00+01:00',
                'id': '20021871',
                'title': 'Jaaropgave',
                'type': '',
                'url': '/focus/document?id=20021871&isBulk=false&isDms=false'
            }
        ]

        self.assertEqual(result, expected)
