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


@patch('focus.focusconnect.Client', new=MockClient)
@patch('focus.focusserver.get_bsn_from_request', new=lambda s: 123456789)  # side step decoding the BSN from SAML token
class CombinedApiTest(FlaskTestCase):
    def create_app(self):
        return application

    def test_combined_api(self):
        self.maxDiff = None
        response = self.client.get('/focus/combined')
        expected = {
            'content': {
                'jaaropgaven': [
                    {
                        'datePublished': '2011-01-28T00:00:00+01:00',
                        'id': '95330222',
                        'title': 'Jaaropgave',
                        'type': '',
                        'url': 'focus/document?id=95330222&isBulk=false&isDms=false'
                    },
                    {
                        'datePublished': '2019-01-04T00:00:00+01:00',
                        'id': '20021871',
                        'title': 'Jaaropgave',
                        'type': '',
                        'url': 'focus/document?id=20021871&isBulk=false&isDms=false'
                    }
                ],
                'uitkeringsspecificaties': [
                    {
                        'datePublished': '2019-04-19T00:00:00+02:00',
                        'id': '24233351',
                        'title': 'Uitkeringsspecificatie',
                        'type': 'Participatiewet',
                        'url': 'focus/document?id=24233351&isBulk=false&isDms=false'
                    },
                    {
                        'datePublished': '2014-01-24T00:00:00+01:00',
                        'id': '30364921',
                        'title': 'Uitkeringsspecificatie',
                        'type': '',
                        'url': 'focus/document?id=30364921&isBulk=false&isDms=false'
                    }
                ],
                'tozodocumenten': [
                    {
                        'datePublished': '2020-03-31T18:59:46+02:00',
                        'description': 'Tegemoetkoming Ondernemers en Zelfstandigen',
                        'id': '4400000031',
                        'type': 'E-AANVR-TOZO',
                        'url': 'focus/document?id=4400000031&isBulk=true&isDms=false'
                    },
                    {
                        'datePublished': '2020-03-26T15:18:44+01:00',
                        'description': 'Verkorte Aanvraag BBZ',
                        'id': '4400000024',
                        'type': 'E-AANVR-KBBZ',
                        'url': 'focus/document?id=4400000024&isBulk=true&isDms=false'
                    },
                    {
                        'datePublished': '2020-03-18T23:09:58+01:00',
                        'description': 'Ondernemerscheck zelfstandigen',
                        'id': '4400000020',
                        'type': 'E-AANVR-DGB',
                        'url': 'focus/document?id=4400000020&isBulk=true&isDms=false'
                    },
                    {
                        'datePublished': '2020-03-31T00:21:51+02:00',
                        'description': 'Tegemoetkoming Ondernemers en Zelfstandigen',
                        'id': '4400000030',
                        'type': 'E-AANVR-TOZO',
                        'url': 'focus/document?id=4400000030&isBulk=true&isDms=false'
                    },
                    {
                        'datePublished': '2020-03-22T00:26:10+01:00',
                        'description': 'Aanvraag BBZ',
                        'id': '4400000022',
                        'type': 'E-AANVR-BBZ',
                        'url': 'focus/document?id=4400000022&isBulk=true&isDms=false'
                    },
                    {
                        'datePublished': '2020-03-31T00:04:34+02:00',
                        'description': 'Tegemoetkoming Ondernemers en Zelfstandigen',
                        'id': '4400000029',
                        'type': 'E-AANVR-TOZO',
                        'url': 'focus/document?id=4400000029&isBulk=true&isDms=false'
                    }
                ]
            },
            'status': 'OK'
        }

        self.assertEqual(response.json, expected)
