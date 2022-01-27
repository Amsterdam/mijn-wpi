from unittest import TestCase
from black import json

# Prepare environment
from mock import patch
from app.config import CustomJSONEncoder

from app.gpass_service import (
    format_budget,
    format_stadspas,
    format_transaction,
    get_admins,
    get_owner_name,
    get_stadspas_admins,
    get_stadspas_details,
    get_transactions,
    send_request,
)
from app.tests.wpi_test_app import MockResponse

# from ..tests.mocks import get_response_mock

TESTKEY = "z4QXWk3bjwFST2HRRVidnn7Se8VFCaHscK39JfODzNs="


class GpassServiceGetStadspas(TestCase):
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


class GpassServiceGetStadspassen(TestCase):
    gpass_pashouder_response = {
        "initialen": "A",
        "achternaam": "Achternaam",
        "passen": [
            {
                "actief": False,
                "pasnummer": 444444444444,
            },
            {
                "actief": True,
                "pasnummer": 333333333333,
            },
        ],
        "sub_pashouders": [
            {
                "initialen": "B",
                "achternaam": "Achternaam",
                "passen": [
                    {
                        "actief": True,
                        "pasnummer": 666666666666,
                    },
                    {
                        "actief": False,
                        "pasnummer": 555555555555,
                    },
                ],
            },
            {
                "initialen": "C",
                "achternaam": "Achternaam",
                "passen": [
                    {
                        "actief": True,
                        "pasnummer": 777777777777,
                    },
                    {
                        "actief": False,
                        "pasnummer": 888888888888,
                    },
                ],
            },
        ],
    }

    gpass_admins = [
        {"owner": "A Achternaam", "admin_number": "xxx", "pass_number": 333333333333},
        {"owner": "B Achternaam", "admin_number": "xxx", "pass_number": 666666666666},
        {"owner": "C Achternaam", "admin_number": "xxx", "pass_number": 777777777777},
    ]

    @patch("app.gpass_service.GPASS_ENDPOINT_PASHOUDER", "http://ha/ha/ha")
    @patch("app.gpass_service.send_request")
    def test_get_stadspas_admins(self, send_request_mock):
        send_request_mock.return_value = self.gpass_pashouder_response

        admin_number = "xxx"
        result = get_stadspas_admins(admin_number)
        expected_path = f"http://ha/ha/ha"

        send_request_mock.assert_called_with(
            expected_path, admin_number, params={"addsubs": True}
        )

        self.assertEqual(result, self.gpass_admins)


class GpassServiceGetTransactions(TestCase):

    gpass_transactions_response = {
        "number_of_items": 20,
        "total_items": 42,
        "transacties": [
            {
                "id": 1,
                "transactiedatum": "2020-10-05T04:01:01.0000",
                "bedrag": 20.0,
                "pashouder": {"id": 1, "hoofd_pashouder_id": 2},
                "pas": {
                    "id": 2,
                    "pasnummer": 6666666666666,
                    "pasnummer_volledig": "66666666666666",
                    "originele_pas": {
                        "id": 1,
                        "pasnummer": 66666666666666,
                        "pasnummer_volledig": "66666666666666",
                    },
                },
                "budget": {
                    "id": 44,
                    "code": "GPAS05_19",
                    "naam": "Schoolactiviteiten",
                    "aanbieder": {"id": 222222, "naam": "Fietsenwinkel - B.V."},
                },
            }
        ],
    }

    gpass_transactions_transformed = [
        {
            "id": 1,
            "title": "Fietsenwinkel - B.V.",
            "amount": 20.0,
            "datePublished": "2020-10-05T04:01:01.0000",
        }
    ]

    @patch("app.gpass_service.GPASS_ENDPOINT_TRANSACTIONS", "http://ha/ha/ha")
    @patch("app.gpass_service.send_request")
    def test_get_transactions(self, send_request_mock):
        send_request_mock.return_value = self.gpass_transactions_response

        transactions = get_transactions("xxx", "111", "abc")
        self.assertEqual(transactions, self.gpass_transactions_transformed)

        send_request_mock.return_value = None

        transactions = get_transactions("xxx", "111", "abc")
        self.assertEqual(transactions, [])


class GpassServiceVarious(TestCase):
    @patch("app.gpass_service.requests.get")
    def test_send_request(self, get_mock):
        get_mock.return_value = MockResponse({"foo": "bar"})

        response = send_request("http://haha", "1x1x1", params={"foo": "bar"})

        get_mock.assert_called_with(
            "http://haha",
            headers={"Authorization": "AppBearer None,1x1x1"},
            timeout=30,
            params={"foo": "bar"},
        )

        self.assertEqual(response, {"foo": "bar"})

    @patch("app.gpass_service.encrypt")
    def test_format_budget(self, encrypt_mock):
        encrypt_mock.return_value = "abcdefghijklmnop"

        budget = {
            "code": "AMSTEG_10-14",
            "naam": "Kindtegoed 10-14",
            "omschrijving": "Kindtegoed",
            "expiry_date": "2021-08-31T21:59:59.000Z",
            "budget_assigned": 150,
            "budget_balance": 0,
        }
        budget_transformed = {
            "description": "Kindtegoed",
            "code": "AMSTEG_10-14",
            "budgetAssigned": 150,
            "budgetBalance": 0,
            "urlTransactions": "/wpi/stadspas/transacties/abcdefghijklmnop",
            "dateEnd": "2021-08-31T21:59:59.000Z",
        }
        admin = {
            "owner": "A Achternaam",
            "admin_number": "xxx",
            "pass_number": 333333333333,
        }
        result = format_budget(budget, admin)

        encrypt_mock.assert_called_with("AMSTEG_10-14", "xxx", 333333333333)

        self.assertEqual(result, budget_transformed)

    @patch("app.gpass_service.format_budget")
    def test_format_stadspas(self, format_budget_mock):
        format_budget_mock.return_value = {"bar": "foo"}
        stadspas = {
            "id": "some-id",
            "pasnummer_volledig": "123123123",
            "budgetten": [{"foo": "bar"}],
            "expiry_date": "2022-01-27T:11:11:11.0000",
        }
        admin = {
            "owner": "A Achternaam",
            "admin_number": "xxx",
            "pass_number": 333333333333,
        }
        stadspas_transformed = {
            "id": "some-id",
            "passNumber": "123123123",
            "owner": "A Achternaam",
            "dateEnd": "2022-01-27T:11:11:11.0000",
            "budgets": [{"bar": "foo"}],
        }

        result = format_stadspas(stadspas, admin)

        format_budget_mock.assert_called_with({"foo": "bar"}, admin)

        self.assertEqual(result, stadspas_transformed)

    def test_get_admins(self):
        admin_number = "12121212"
        owner_name = "John Kelly"
        stadspassen = [
            {
                "actief": False,
                "pasnummer": 444444444444,
            },
            {
                "actief": True,
                "pasnummer": 333333333333,
            },
        ]
        result = get_admins(admin_number, owner_name, stadspassen)

        self.assertEqual(
            result,
            [
                {
                    "owner": "John Kelly",
                    "admin_number": "12121212",
                    "pass_number": 333333333333,
                }
            ],
        )

        stadspassen = [
            {
                "actief": False,
                "pasnummer": 444444444444,
            },
            {
                "actief": False,
                "pasnummer": 333333333333,
            },
        ]
        result = get_admins(admin_number, owner_name, stadspassen)

        self.assertEqual(
            result,
            [],
        )

    def test_get_owner_name(self):
        name = get_owner_name({"volledige_naam": "John Kelly"})
        self.assertEqual(name, "John Kelly")

        name = get_owner_name({"achternaam": "Kenedy", "initialen": "J F"})
        self.assertEqual(name, "J F Kenedy")
