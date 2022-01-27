from unittest import TestCase
from black import json

# Prepare environment
from mock import patch
from app.config import CustomJSONEncoder

from app.gpass_service import get_stadspas_details
from app.tests.wpi_test_app import FERNET_KEY_MOCK
from freezegun import freeze_time

# from ..tests.mocks import get_response_mock

TESTKEY = "z4QXWk3bjwFST2HRRVidnn7Se8VFCaHscK39JfODzNs="


class GpassServiceTest(TestCase):
    gpass_pas_response = {
        "actief": True,
        "balance_update_time": "2020-04-02T12:45:41.000Z",
        "budgetten": [
            {
                "code": "AMSTEG_10-14",
                "naam": "Kindtegoed 10-14",
                "omschrijving": "Kindtegoed",
                "expiry_date": "2021-08-31T21:59:59.000Z",
                "budget_assigned": 150,
                "budget_balance": 0,
            }
        ],
        "budgetten_actief": True,
        "categorie": "Amsterdamse Digitale Stadspas",
        "categorie_code": "A",
        "expiry_date": "2020-08-31T23:59:59.000Z",
        "id": 999999,
        "originele_pas": {
            "categorie": "Amsterdamse Digitale Stadspas",
            "categorie_code": "A",
            "id": 888888,
            "pasnummer": 8888888888888,
            "pasnummer_volledig": "8888888888888888888",
            "passoort": {"id": 11, "naam": "Digitale Stadspas"},
        },
        "pasnummer": 6666666666666,
        "pasnummer_volledig": "6666666666666666666",
        "passoort": {"id": 11, "naam": "Digitale Stadspas"},
    }

    gpass_formatted = {
        "id": 999999,
        "passNumber": "6666666666666666666",
        "owner": "N T Koop",
        "dateEnd": "2020-08-31T23:59:59.000Z",
        "budgets": [
            {
                "description": "Kindtegoed",
                "code": "AMSTEG_10-14",
                "budgetAssigned": 150,
                "budgetBalance": 0,
                "urlTransactions": "/wpi/stadspas/transacties/abcdefghijklmnop",
                "dateEnd": "2021-08-31T21:59:59.000Z",
            }
        ],
    }

    @patch("app.gpass_service.GPASS_ENDPOINT_PAS", "http://ha/ha/ha")
    @patch("app.gpass_service.encrypt")
    @patch("app.gpass_service.send_request")
    def test_get_stadspas_details(self, send_request_mock, encrypt_mock):
        send_request_mock.return_value = self.gpass_pas_response
        encrypt_mock.return_value = "abcdefghijklmnop"

        admin = {
            "admin_number": "111111111111",
            "pass_number": "222222222222",
            "owner": "N T Koop",
        }

        result = get_stadspas_details(admin)
        pass_number = admin["pass_number"]
        expected_path = f"http://ha/ha/ha{pass_number}"

        send_request_mock.assert_called_with(
            expected_path, admin["admin_number"], params={"include_balance": True}
        )

        self.assertEqual(
            result["budgets"][0]["urlTransactions"],
            "/wpi/stadspas/transacties/abcdefghijklmnop",
        )

        self.assertEqual(result, self.gpass_formatted)

    # def test_get_transactions(self):
    #     pas_number = "6666666666666"
    #     budget_code = "aaa"
    #     result = get_transactions(self.admin_number, pas_number, budget_code)

    #     expected = [
    #         {
    #             "id": 1,
    #             "title": "Fietsenwinkel - B.V.",
    #             "amount": 20.0,
    #             "date": "2020-10-05T04:01:01.0000000",
    #         }
    #     ]
    #     self.assertEqual(result, expected)

    # def test_get_transactions_wrong_pas_number(self):
    #     pas_number = 11111
    #     result = get_transactions(self.admin_number, pas_number, budget_code="aaa")
    #     self.assertEqual(result, [])


# @patch("app.gpass_service.GPASS_API_LOCATION", "http://localhost")
# @patch("app.gpass_service.requests.get", get_response_mock)
# @patch("app.utils.GPASS_FERNET_ENCRYPTION_KEY", TESTKEY)
# class GpassApiTest(WpiApiTestApp):
#     admin_number = "111111111"
#     pas_number = "6666666666666"
#     budget_code = "aaa"

#     def test_get_transactions(self):
#         encrypted = encrypt(self.budget_code, self.admin_number, self.pas_number)
#         response = self.client.get(f"/focus/stadspastransacties/{encrypted}")

#         expected = {
#             "content": [
#                 {
#                     "amount": 20.0,
#                     "date": "2020-10-05T04:01:01.0000000",
#                     "id": 1,
#                     "title": "Fietsenwinkel - B.V.",
#                 }
#             ],
#             "status": "OK",
#         }

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, expected)
