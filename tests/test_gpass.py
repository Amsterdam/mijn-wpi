from unittest import TestCase

# Prepare environment
from mock import patch

from app.utils import encrypt
from app.gpass_service import get_stadspassen, get_transactions
from tests.focus_test_app import FocusApiTestApp

from .mocks import get_response_mock

TESTKEY = "z4QXWk3bjwFST2HRRVidnn7Se8VFCaHscK39JfODzNs="


@patch("app.gpass_service.GPASS_API_LOCATION", "http://localhost")
@patch("app.gpass_service.requests.get", get_response_mock)
@patch("app.utils.GPASS_FERNET_ENCRYPTION_KEY", TESTKEY)
class GpassServiceTest(TestCase):
    admin_number = "111111111"

    def test_get_stadspassen(self):
        result = get_stadspassen(self.admin_number)

        expected = [
            {
                "budgets": [
                    {
                        "code": "AMSTEG_10-14",
                        "description": "Kindtegoed",
                        "datumAfloop": "2021-08-31T21:59:59.000Z",
                        "assigned": 150,
                        "balance": 0,
                    }
                ],
                "datumAfloop": "2020-08-31T23:59:59.000Z",
                "id": 999997,
                "naam": "J. Doe",
                "pasnummer": "6011012604737",
            },
            {
                "budgets": [
                    {
                        "code": "AMSTEG_10-14",
                        "description": "Kindtegoed",
                        "datumAfloop": "2021-08-31T21:59:59.000Z",
                        "assigned": 150,
                        "balance": 0,
                    }
                ],
                "datumAfloop": "2020-08-31T23:59:59.000Z",
                "id": 999999,
                "naam": "P Achternaam2",
                "pasnummer": "6666666666666666666",
            },
            {
                "budgets": [
                    {
                        "code": "AMSTEG_10-14",
                        "description": "Kindtegoed",
                        "datumAfloop": "2021-08-31T21:59:59.000Z",
                        "assigned": 150,
                        "balance": 0,
                    }
                ],
                "datumAfloop": "2020-08-31T23:59:59.000Z",
                "id": 999997,
                "naam": "J Achternaam3",
                "pasnummer": "6011012604737",
            },
        ]

        self.assertTrue(
            result[0]["budgets"][0]["urlTransactions"].startswith(
                "/api/focus/stadspastransacties/"
            )
        )
        # remove url, it has a timebased factor in it.
        del result[0]["budgets"][0]["urlTransactions"]
        del result[1]["budgets"][0]["urlTransactions"]
        del result[2]["budgets"][0]["urlTransactions"]

        self.assertEqual(result, expected)

    def test_get_transactions(self):
        pas_number = "6666666666666"
        budget_code = "aaa"
        result = get_transactions(self.admin_number, pas_number, budget_code)

        expected = [
            {
                "id": 1,
                "title": "Fietsenwinkel - B.V.",
                "amount": 20.0,
                "date": "2020-10-05T04:01:01.0000000",
            }
        ]
        self.assertEqual(result, expected)

    def test_get_transactions_wrong_pas_number(self):
        pas_number = 11111
        result = get_transactions(self.admin_number, pas_number, budget_code="aaa")
        self.assertEqual(result, [])


@patch("app.gpass_service.GPASS_API_LOCATION", "http://localhost")
@patch("app.gpass_service.requests.get", get_response_mock)
@patch("app.utils.GPASS_FERNET_ENCRYPTION_KEY", TESTKEY)
class GpassApiTest(FocusApiTestApp):
    admin_number = "111111111"
    pas_number = "6666666666666"
    budget_code = "aaa"

    def test_get_transactions(self):
        encrypted = encrypt(self.budget_code, self.admin_number, self.pas_number)
        response = self.client.get(f"/focus/stadspastransacties/{encrypted}")

        expected = {
            "content": [
                {
                    "amount": 20.0,
                    "date": "2020-10-05T04:01:01.0000000",
                    "id": 1,
                    "title": "Fietsenwinkel - B.V.",
                }
            ],
            "status": "OK",
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected)
