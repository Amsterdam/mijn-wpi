import datetime
from unittest import TestCase
from unittest.mock import patch

from app.focus_service_stadspas_admin import (
    get_first_pas_type,
    get_stadspas_admin_number,
    has_groene_stip,
)
from app.tests.wpi_test_app import MockClient


class TestFocusStadspasAdmin(TestCase):
    def test_has_groene_stip(self):
        result = has_groene_stip(example_response["fondsen"]["fonds"])
        self.assertTrue(result)

    def test_get_first_pas_type(self):
        result = get_first_pas_type(example_response["fondsen"]["fonds"])
        self.assertEqual(result, "kind")

    @patch("app.focus_service_stadspas_admin.get_client")
    def test_get_stadspas_admin_number(self, get_client_mock):
        mock_client = MockClient(
            name="getStadspas",
            response=example_response2,
        )
        get_client_mock.return_value = mock_client
        result = get_stadspas_admin_number("11xx11")

        mock_client.service.getStadspas.assert_called_with(bsn="11xx11")

        self.assertEqual(result, {"type": "hoofdpashouder", "admin_number": 123123123})


example_response = {
    "administratienummer": 123123123,
    "bsn": 12312312399,
    "fondsen": {
        "fonds": [
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 180572,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 180573,
                "soortFonds": 3557,
            },
        ]
    },
}


example_response2 = {
    "administratienummer": 123123123,
    "bsn": 12312312399,
    "fondsen": {
        "fonds": [
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 384018,
                "soortFonds": 3555,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2018, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2019, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 1609546,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2018, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2019, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 1609547,
                "soortFonds": 3555,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 381271,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2019, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2020, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 740599,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2019, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2020, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 757447,
                "soortFonds": 3555,
            },
        ]
    },
}
