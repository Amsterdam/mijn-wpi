import os.path
from unittest import TestCase

# Prepare environment
from flask_testing import TestCase as FlaskTestCase
from mock import patch

from tests.mocks import MockClient

os.environ['FOCUS_USERNAME'] = 'FOCUS_USERNAME'
os.environ['FOCUS_PASSWORD'] = 'FOCUS_PASSWORD'
os.environ['FOCUS_WSDL'] = 'focus/focus.wsdl'
os.environ['TMA_CERTIFICATE'] = __file__

from focus.config import config, credentials  # noqa: E402  Module level import not at top of file
from focus.focusconnect import FocusConnection  # noqa: E402
from focus.server import application  # noqa: E402


@patch('focus.focusconnect.Client', new=MockClient)
class JaaropgavenTest(TestCase):
    def test_connection(self):
        focus_connection = FocusConnection(config, credentials)
        result = focus_connection.jaaropgaven(bsn=1234, url_root='/')
        expected = [
            {
                'datePublished': '2011-01-28T00:00:00+01:00',
                'id': '172065',
                'title': 'Jaaropgave',
                'type': '',
                'url': '/focus/document?id=172065&isBulk=false&isDms=false'
            },
            {
                'datePublished': '2019-01-04T00:00:00+01:00',
                'id': '172065',
                'title': 'Jaaropgave',
                'type': '',
                'url': '/focus/document?id=172065&isBulk=false&isDms=false'
            }
        ]

        self.assertEqual(result, expected)


@patch('focus.focusconnect.Client', new=MockClient)
@patch('focus.focusserver.get_bsn_from_request', new=lambda s: 123456789)  # side step decoding the BSN from SAML token
class CombinedApiTest(FlaskTestCase):
    def create_app(self):
        return application

    def test_combined_api(self):
        response = self.client.get('/focus/combined')
        expected = {
            'content': {
                'jaaropgaven': [
                    {
                        'datePublished': '2011-01-28T00:00:00+01:00',
                        'id': '172065',
                        'title': 'Jaaropgave',
                        'type': '',
                        'url': 'focus/document?id=172065&isBulk=false&isDms=false'
                    },
                    {
                        'datePublished': '2019-01-04T00:00:00+01:00',
                        'id': '172065',
                        'title': 'Jaaropgave',
                        'type': '',
                        'url': 'focus/document?id=172065&isBulk=false&isDms=false'
                    }
                ],
                'uitkeringsspecificaties': [
                    {
                        'datePublished': '2019-04-19T00:00:00+02:00',
                        'id': '172013',
                        'title': 'Uitkeringsspecificatie',
                        'type': 'Participatiewet',
                        'url': 'focus/document?id=172013&isBulk=false&isDms=false'
                    },
                    {
                        'datePublished': '2014-01-24T00:00:00+01:00',
                        'id': '172013',
                        'title': 'Uitkeringsspecificatie',
                        'type': '',
                        'url': 'focus/document?id=172013&isBulk=false&isDms=false'
                    }
                ]
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected)
