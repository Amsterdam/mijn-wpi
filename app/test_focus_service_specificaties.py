import datetime
from unittest import TestCase
from unittest.mock import patch

from app.focus_service_specificaties import get_jaaropgaven, get_uitkeringsspecificaties
from app.test_app import MockClient


def create_specificatie(omschrijving, id, einddatumDocument):
    return {
        "id": id,
        "documentCode": {
            "omschrijving": omschrijving,
        },
        "einddatumDocument": einddatumDocument,
        "variant": None,
    }


def create_example_soap_response(documents):
    return {"document": documents}


class TestSpecificatieService(TestCase):
    @patch("app.focus_service_specificaties.get_e_aanvragen_raw")
    @patch("app.focus_service_specificaties.get_client")
    def test_get_jaaropgaven(self, get_client_mock, get_focus_specificaties_mock):
        spec1 = create_specificatie("test1", "1a", datetime.datetime(2020, 1, 5, 0, 0))
        spec2 = create_specificatie("test2", "1b", datetime.datetime(2021, 1, 9, 0, 0))

        get_focus_specificaties_mock.return_value = [
            {
                "datumDocument": datetime.datetime(2020, 4, 3, 17, 20, 4),
                "documentCodes": {
                    "documentCode": "7025",
                    "documentCodeId": "177025",
                    "documentOmschrijving": "Jaaropgave 1",
                },
                "documentId": 660000000000058,
                "isBulk": False,
                "isDms": False,
                "variant": None,
            },
            {
                "datumDocument": datetime.datetime(2020, 10, 27, 17, 20, 4),
                "documentCodes": {
                    "documentCode": "6026",
                    "documentCodeId": "176026",
                    "documentOmschrijving": "Jaaropgave 2",
                },
                "documentId": 660000000000099,
                "isBulk": False,
                "isDms": False,
                "variant": None,
            },
        ]

        mock_client = MockClient(
            response=create_example_soap_response([spec1, spec2]),
            name="getJaaropgaven",
        )

        get_client_mock.return_value = mock_client

        bsn = "12312312399"
        result = get_jaaropgaven(bsn)

        mock_client.service.getJaaropgaven.assert_called_with(bsn)

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["title"], "test1 2019")
        self.assertEqual(result[1]["title"], "test2 2020")
        self.assertEqual(result[2]["title"], "Jaaropgave 2019 rentedragende lening Bbz")
        self.assertEqual(
            result[3]["title"], "Jaaropgave 2019 rentedragende lening Tozo"
        )

    @patch("app.focus_service_specificaties.handle_soap_service_error")
    @patch("app.focus_service_specificaties.get_client")
    def test_get_jaaropgaven_error(
        self, get_client_mock, handle_soap_service_error_mock
    ):
        mock_client = MockClient(
            response=None,
            name="getJaaropgaven",
        )

        get_client_mock.return_value = mock_client

        bsn = "12312312399"
        get_jaaropgaven(bsn)

        mock_client.service.getJaaropgaven.assert_called_with(bsn)
        handle_soap_service_error_mock.assert_called()

    @patch("app.focus_service_specificaties.get_client")
    def test_get_uitkeringsspecificaties(self, get_client_mock):
        spec1 = create_specificatie("test1", "1a", datetime.datetime(2020, 1, 5, 0, 0))
        spec2 = create_specificatie("test2", "1b", datetime.datetime(2020, 2, 6, 0, 0))

        mock_client = MockClient(
            response=create_example_soap_response([spec1, spec2]),
            name="getUitkeringspecificaties",
        )

        get_client_mock.return_value = mock_client

        bsn = "12312312399"
        result = get_uitkeringsspecificaties(bsn)

        mock_client.service.getUitkeringspecificaties.assert_called_with(bsn)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "test1 Januari-2020")
        self.assertEqual(result[1]["title"], "test2 Februari-2020")

    @patch("app.focus_service_specificaties.handle_soap_service_error")
    @patch("app.focus_service_specificaties.get_client")
    def test_get_uitkeringsspecificaties_error(
        self, get_client_mock, handle_soap_service_error_mock
    ):
        mock_client = MockClient(
            response=None,
            name="getUitkeringspecificaties",
        )

        get_client_mock.return_value = mock_client

        bsn = "12312312399"
        get_uitkeringsspecificaties(bsn)

        mock_client.service.getUitkeringspecificaties.assert_called_with(bsn)
        handle_soap_service_error_mock.assert_called()
