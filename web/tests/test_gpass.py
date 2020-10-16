from unittest import TestCase

# Prepare environment
from flask_testing import TestCase as FlaskTestCase
from mock import patch

from focus.gpass_connect import GpassConnection
from .mocks import MockClient, get_response_mock

from focus.server import application  # noqa: E402


@patch('focus.gpass_connect.requests.get', get_response_mock)
class GpassConnectionTest(TestCase):
    admin_number = '111111111'

    def setUp(self) -> None:
        pass

    def _get_connection(self):
        return GpassConnection('http://localhost', 'token')

    def test_get_stadspassen(self):
        con = self._get_connection()
        result = con.get_stadspassen(self.admin_number)

        expected = [
            {
                'id': 999999,
                'pasnummer': 6666666666666,
                'datumAfloop': '2020-08-31T23:59:59.000Z',
                'naam': 'A Achternaam',
                'budgets': [
                    {
                        'description': 'Educatie budget, voor iedereen uit de gemeente amsterdam en geboren tussen 1-1-2004 en 1-1-2020',
                        'code': 'AMSEducatie',
                        'assigned': 100,
                        'balance': 0
                    }
                ]
            }
        ]

        self.assertEqual(result, expected)

    def test_get_transactions(self):
        pas_number = 6666666666666
        con = self._get_connection()
        result = con.get_transactions(self.admin_number, pas_number)

        expected = [
            {
                'id': 1,
                'title': 'title',
                'amount': 20.0,
                'date': '2020-10-05T04:01:01.0000000'
            }
        ]
        self.assertEqual(result, expected)

    def test_get_transactions_wrong_pas_number(self):
        pas_number = 11111
        con = self._get_connection()
        result = con.get_transactions(self.admin_number, pas_number)
        self.assertEqual(result, None)


class GpassApiTest(FlaskTestCase):
    def create_app(self):
        return application

    # stadpassen data is in the combined api

    def test_get_transactions(self):
        response = self.client.get('/focus/stadspastransacties')

        expected = {
            'status': 'OK',
            'content': [],
        }
        self.assert200(response)
        self.assertEqual(response.json, expected)
