import datetime
from unittest import TestCase
from unittest.mock import call, patch

from app.focus_service_e_aanvraag import (
    create_e_aanvraag,
    get_document_config,
    get_e_aanvraag_step,
    get_e_aanvragen,
    get_steps_collection,
)
from app.tests.wpi_test_app import MockClient, create_soap_response_get_aanvragen


class FocusSerivceEAanvraag(TestCase):
    maxDiff = None

    def test_get_document_config(self):
        document_code_id = 176182
        document_config = get_document_config(document_code_id)

        self.assertEqual(document_config["product"], "tonk")
        self.assertEqual(document_config["step_type"], "besluit")
        self.assertEqual(document_config["decision"], "toekenning")

        document_config = get_document_config(123)

        self.assertIsNone(document_config)

    def test_get_steps_collection(self):
        collection = get_steps_collection()
        self.assertEqual(
            collection,
            {
                "tozo 1": [],
                "tozo 2": [],
                "tozo 3": [],
                "tozo 4": [],
                "tozo 5": [],
                "tonk": [],
                "bbz": [],
                "ioaz": [],
            },
        )

    def test_create_e_aanvraag(self):

        product_name = "tozo 5"
        steps = [
            {
                "id": "1x1",
                "title": "Aanvraag document",
                "datePublished": datetime.datetime(2020, 10, 23, 17, 20, 4),
                "status": "aanvraag",
                "documents": [],
            }
        ]
        result_expected = {
            "title": "Tozo 5 (aangevraagd vanaf 1 juli 2021)",
            "id": "d7263e1172ef87e1a570f8cf1710b29a",
            "dateStart": "2020-10-23T17:20:04",
            "datePublished": "2020-10-23T17:20:04",
            "dateEnd": None,
            "decision": None,
            "status": "aanvraag",
            "steps": [
                {
                    "id": "1x1",
                    "title": "Aanvraag document",
                    "datePublished": "2020-10-23T17:20:04",
                    "title": "aanvraag",
                    "documents": [],
                }
            ],
        }
        result = create_e_aanvraag(product_name, steps)
        self.assertEqual(result, result_expected)

    def test_create_e_aanvraag(self):
        product_name = "tonk"
        steps = [
            {
                "id": "1x1",
                "title": "Aanvraag document",
                "datePublished": datetime.datetime(2020, 10, 23, 17, 20, 4),
                "title": "aanvraag",
                "documents": [],
            },
            {
                "id": "1x2",
                "title": "Besluit document",
                "datePublished": datetime.datetime(2020, 11, 15, 10, 00, 2),
                "title": "besluit",
                "documents": [],
                "decision": "toekenning",
            },
        ]
        result_expected = {
            "title": "TONK",
            "id": "35243ffdb3668fc3f4607e7c41dea31e",
            "dateStart": "2020-10-23T17:20:04",
            "datePublished": "2020-11-15T10:00:02",
            "dateEnd": "2020-11-15T10:00:02",
            "decision": "toekenning",
            "status": "besluit",
            "steps": [
                {
                    "id": "1x1",
                    "title": "Aanvraag document",
                    "datePublished": "2020-10-23T17:20:04",
                    "title": "aanvraag",
                    "documents": [],
                },
                {
                    "id": "1x2",
                    "title": "Besluit document",
                    "datePublished": "2020-11-15T10:00:02",
                    "title": "besluit",
                    "decision": "toekenning",
                    "documents": [],
                },
            ],
        }
        result = create_e_aanvraag(product_name, steps)
        self.assertEqual(result, result_expected)

    def test_get_e_aanvraag_step(self):
        e_aanvraag = {
            "datumDocument": datetime.datetime(2020, 10, 27, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5364",
                "documentCodeId": "175364",
                "documentOmschrijving": "Tozo3 Afwijzen",
            },
            "documentId": 660000000000099,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        }

        document_code_id = "175364"
        document_config = {
            "omschrijving": "Tozo3 Afwijzen",
            "step_type": "besluit",
            "product": "Tozo 3",
            "document_title": "Besluit afwijzing",
            "decision": "afwijzing",
        }

        result_expected = {
            "id": "175364",
            "title": "besluit",
            "datePublished": datetime.datetime(2020, 10, 27, 17, 20, 4),
            "decision": "afwijzing",
            "documents": [
                {
                    "id": "660000000000099",
                    "title": "Besluit afwijzing",
                    "datePublished": "2020-10-27T17:20:04",
                    "url": "/wpi/aanvraag/document?id=660000000000099&isBulk=False&isDms=False",
                }
            ],
        }

        result = get_e_aanvraag_step(e_aanvraag, document_code_id, document_config)

        self.assertEqual(result, result_expected)

    @patch("app.focus_service_e_aanvraag.logging.error")
    @patch("app.focus_service_e_aanvraag.get_client")
    def test_get_e_aanvragen(self, get_client_mock, log_error_mock):
        mock_client = MockClient(
            response=example_soap_response, name="getEAanvraagTozo"
        )
        get_client_mock.return_value = mock_client
        bsn = "123xx123"
        result = get_e_aanvragen(bsn)
        mock_client.service.getEAanvraagTozo.assert_called_with(bsn)
        log_error_mock.assert_has_calls(
            [
                call("Unknown E_Aanvraag Document encountered 176371"),
                call("Unknown E_Aanvraag Document encountered 176372"),
            ]
        )
        self.assertEqual(log_error_mock.call_count, 2)
        self.assertEqual(result, example_result)


example_soap_response = {
    "bsn": 12312312323,
    "documentgegevens": [
        {
            "datumDocument": datetime.datetime(2020, 4, 3, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5296",
                "documentCodeId": "175296",
                "documentOmschrijving": "Tozo Toekennen voorschot",
            },
            "documentId": 660000000000058,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 10, 27, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5364",
                "documentCodeId": "175364",
                "documentOmschrijving": "Tozo3 Afwijzen",
            },
            "documentId": 660000000000099,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 8, 10, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "6182",
                "documentCodeId": "176182",
                "documentOmschrijving": "TONK Besluit over verlenging",
            },
            "documentId": 660000000010184,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 9, 3, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "112",
                    "documentCategorieNaam": "Declaratie",
                },
                "documentCode": "6371",
                "documentCodeId": "176371",
                "documentOmschrijving": "Bbz toekennen PU via batch",
            },
            "documentId": 660000000010236,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 10, 23, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5309",
                "documentCodeId": "175309",
                "documentOmschrijving": "Tozo3 Toekennen",
            },
            "documentId": 660000000000098,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 4, 8, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5651",
                "documentCodeId": "175651",
                "documentOmschrijving": "Tozo4 Afwijzen",
            },
            "documentId": 660000000000473,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 8, 12, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "26182",
                "documentCodeId": "1726182",
                "documentOmschrijving": "TONK Bevestigen weigering verlenging",
            },
            "documentId": 660000000010185,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 7, 3, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5336",
                "documentCodeId": "175336",
                "documentOmschrijving": "Tozo2 Toekennen",
            },
            "documentId": 660000000000076,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 9, 2, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "102",
                    "documentCategorieNaam": "Kennisgeving",
                },
                "documentCode": "5855",
                "documentCodeId": "175855",
                "documentOmschrijving": "Bbz Verlenging beslistermijn met 13 weken",
            },
            "documentId": 660000000010211,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 9, 16, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "123",
                    "documentCategorieNaam": "Informatieverzoek bij klant",
                },
                "documentCode": "6322",
                "documentCodeId": "176322",
                "documentOmschrijving": "Ioaz Aanvraag hersteltermijn",
            },
            "documentId": 660000000010212,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 4, 4, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5677",
                "documentCodeId": "175677",
                "documentOmschrijving": "Tozo4 Toekennen voorschot via batch",
            },
            "documentId": 660000000000471,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 10, 19, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5372",
                "documentCodeId": "175372",
                "documentOmschrijving": "Tozo3 Toekennen voorschot via batch",
            },
            "documentId": 660000000000097,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 9, 4, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "112",
                    "documentCategorieNaam": "Declaratie",
                },
                "documentCode": "6372",
                "documentCodeId": "176372",
                "documentOmschrijving": "Bbz toekennen voorschot via batch",
            },
            "documentId": 660000000010237,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 6, 23, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5345",
                "documentCodeId": "175345",
                "documentOmschrijving": "Tozo2 Toekennen voorschot via batch",
            },
            "documentId": 660000000000413,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 4, 8, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5303",
                "documentCodeId": "175303",
                "documentOmschrijving": "Tozo Toekennen",
            },
            "documentId": 660000000000059,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 7, 8, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "6165",
                "documentCodeId": "176165",
                "documentOmschrijving": "Tozo5 Afwijzen",
            },
            "documentId": 660000000000055,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 4, 6, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5654",
                "documentCodeId": "175654",
                "documentOmschrijving": "Tozo4 Toekennen",
            },
            "documentId": 660000000000472,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 1, 7, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "6146",
                "documentCodeId": "176146",
                "documentOmschrijving": "TONK Buiten behandeling laten",
            },
            "documentId": 660000000000501,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 7, 4, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "6171",
                "documentCodeId": "176171",
                "documentOmschrijving": "Tozo5 Toekennen voorschot via batch",
            },
            "documentId": 660000000000053,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 1, 6, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "137",
                "documentCodeId": "176137",
                "documentOmschrijving": "TONK Hersteltermijn",
            },
            "documentId": 660000000000500,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 7, 6, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "6167",
                "documentCodeId": "176167",
                "documentOmschrijving": "Tozo5 Toekennen",
            },
            "documentId": 660000000000054,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 7, 4, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "101",
                    "documentCategorieNaam": "Besluit",
                },
                "documentCode": "5337",
                "documentCodeId": "175337",
                "documentOmschrijving": "Tozo2 Afwijzen",
            },
            "documentId": 660000000000077,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 1, 5, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "E-AANVR-TONK1",
                "documentCodeId": "802",
                "documentOmschrijving": "TONK 1 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
            },
            "documentId": 4400000095,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 3, 27, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "E-AANVR-TOZO",
                "documentCodeId": "770",
                "documentOmschrijving": "Tegemoetkoming Ondernemers en Zelfstandigen ",
            },
            "documentId": 4400000027,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 10, 14, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "E-AANVR-TOZ3",
                "documentCodeId": "785",
                "documentOmschrijving": "TOZO 3 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
            },
            "documentId": 4400000053,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 4, 2, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "E-AANVR-TOZO",
                "documentCodeId": "770",
                "documentOmschrijving": "Tegemoetkoming Ondernemers en Zelfstandigen ",
            },
            "documentId": 4400000033,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 4, 1, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "E-AANVR-TOZO",
                "documentCodeId": "770",
                "documentOmschrijving": "Tegemoetkoming Ondernemers en Zelfstandigen ",
            },
            "documentId": 4400000034,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 7, 2, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "TOZ5",
                "documentCodeId": "837",
                "documentOmschrijving": "TOZO 5 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
            },
            "documentId": 4400000123,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2020, 6, 19, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "E-AANVR-TOZ2",
                "documentCodeId": "777",
                "documentOmschrijving": "TOZO 2 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
            },
            "documentId": 4400000071,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 8, 8, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "109",
                    "documentCategorieNaam": "Overige",
                },
                "documentCode": "TONK_CORR",
                "documentCodeId": "843",
                "documentOmschrijving": "Correctiemail Tonk",
            },
            "documentId": 4400000132,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 4, 2, 18, 53, 5),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "E-AANVR-TOZ4",
                "documentCodeId": "800",
                "documentOmschrijving": "TOZO 4 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
            },
            "documentId": 4400000022,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 9, 1, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "BBZ2",
                "documentCodeId": "844",
                "documentOmschrijving": "Aanvraag BBZ2",
            },
            "documentId": 4400000146,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
        {
            "datumDocument": datetime.datetime(2021, 9, 15, 17, 20, 4),
            "documentCodes": {
                "documentCategorie": {
                    "documentCategorieCode": "116",
                    "documentCategorieNaam": "Aanvraag",
                },
                "documentCode": "BBZ2",
                "documentCodeId": "844",
                "documentOmschrijving": "Aanvraag BBZ2",
            },
            "documentId": 4400000147,
            "isBulk": True,
            "isDms": False,
            "variant": None,
        },
    ],
}

example_result = [
    {
        "id": "953311469171d5f297fcad251f3310a1",
        "title": "Tozo 1 (aangevraagd voor 1 juni 2020)",
        "dateStart": "2020-03-27T17:20:04",
        "datePublished": "2020-04-08T17:20:04",
        "dateEnd": "2020-04-08T17:20:04",
        "decision": "toekenning",
        "status": "besluit",
        "steps": [
            {
                "id": "770",
                "title": "aanvraag",
                "datePublished": "2020-03-27T17:20:04",
                "documents": [
                    {
                        "id": "4400000027",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-03-27T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000027&isBulk=True&isDms=False",
                        "datePublished": "2020-03-27T17:20:04",
                    },
                    {
                        "id": "4400000034",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-04-01T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000034&isBulk=True&isDms=False",
                        "datePublished": "2020-04-01T17:20:04",
                    },
                    {
                        "id": "4400000033",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-04-02T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000033&isBulk=True&isDms=False",
                        "datePublished": "2020-04-02T17:20:04",
                    },
                ],
            },
            {
                "id": "175296",
                "title": "voorschot",
                "datePublished": "2020-04-03T17:20:04",
                "documents": [
                    {
                        "id": "660000000000058",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/aanvraag/document?id=660000000000058&isBulk=False&isDms=False",
                        "datePublished": "2020-04-03T17:20:04",
                    }
                ],
            },
            {
                "id": "175303",
                "title": "besluit",
                "datePublished": "2020-04-08T17:20:04",
                "documents": [
                    {
                        "id": "660000000000059",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/aanvraag/document?id=660000000000059&isBulk=False&isDms=False",
                        "datePublished": "2020-04-08T17:20:04",
                    }
                ],
                "decision": "toekenning",
            },
        ],
    },
    {
        "id": "ee5dc44e435040731d39b84e0fd0b4f5",
        "title": "Tozo 2 (aangevraagd vanaf 1 juni 2020)",
        "dateStart": "2020-06-19T17:20:04",
        "datePublished": "2020-07-04T17:20:04",
        "dateEnd": "2020-07-04T17:20:04",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "777",
                "title": "aanvraag",
                "datePublished": "2020-06-19T17:20:04",
                "documents": [
                    {
                        "id": "4400000071",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-06-19T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000071&isBulk=True&isDms=False",
                        "datePublished": "2020-06-19T17:20:04",
                    }
                ],
            },
            {
                "id": "175345",
                "title": "voorschot",
                "datePublished": "2020-06-23T17:20:04",
                "documents": [
                    {
                        "id": "660000000000413",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/aanvraag/document?id=660000000000413&isBulk=False&isDms=False",
                        "datePublished": "2020-06-23T17:20:04",
                    }
                ],
            },
            {
                "id": "175336",
                "title": "besluit",
                "datePublished": "2020-07-03T17:20:04",
                "documents": [
                    {
                        "id": "660000000000076",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/aanvraag/document?id=660000000000076&isBulk=False&isDms=False",
                        "datePublished": "2020-07-03T17:20:04",
                    }
                ],
                "decision": "toekenning",
            },
            {
                "id": "175337",
                "title": "besluit",
                "datePublished": "2020-07-04T17:20:04",
                "documents": [
                    {
                        "id": "660000000000077",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/aanvraag/document?id=660000000000077&isBulk=False&isDms=False",
                        "datePublished": "2020-07-04T17:20:04",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "27c726a8ee4dd93a48c9f3c30cf865b2",
        "title": "Tozo 3 (aangevraagd vanaf 1 oktober 2020)",
        "dateStart": "2020-10-14T17:20:04",
        "datePublished": "2020-10-27T17:20:04",
        "dateEnd": "2020-10-27T17:20:04",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "785",
                "title": "aanvraag",
                "datePublished": "2020-10-14T17:20:04",
                "documents": [
                    {
                        "id": "4400000053",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-10-14T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000053&isBulk=True&isDms=False",
                        "datePublished": "2020-10-14T17:20:04",
                    }
                ],
            },
            {
                "id": "175372",
                "title": "voorschot",
                "datePublished": "2020-10-19T17:20:04",
                "documents": [
                    {
                        "id": "660000000000097",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/aanvraag/document?id=660000000000097&isBulk=False&isDms=False",
                        "datePublished": "2020-10-19T17:20:04",
                    }
                ],
            },
            {
                "id": "175309",
                "title": "besluit",
                "datePublished": "2020-10-23T17:20:04",
                "documents": [
                    {
                        "id": "660000000000098",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/aanvraag/document?id=660000000000098&isBulk=False&isDms=False",
                        "datePublished": "2020-10-23T17:20:04",
                    }
                ],
            },
            {
                "id": "175364",
                "title": "besluit",
                "datePublished": "2020-10-27T17:20:04",
                "documents": [
                    {
                        "id": "660000000000099",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/aanvraag/document?id=660000000000099&isBulk=False&isDms=False",
                        "datePublished": "2020-10-27T17:20:04",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "e9fabddf1d6e9386622faeba4c945c48",
        "title": "Tozo 4 (aangevraagd vanaf 1 april 2021)",
        "dateStart": "2021-04-02T18:53:05",
        "datePublished": "2021-04-08T18:53:05",
        "dateEnd": "2021-04-08T18:53:05",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "800",
                "title": "aanvraag",
                "datePublished": "2021-04-02T18:53:05",
                "documents": [
                    {
                        "id": "4400000022",
                        "title": "Ontvangst- bevestiging Aanvraag\n2021-04-02T18:53:05",
                        "url": "/wpi/aanvraag/document?id=4400000022&isBulk=True&isDms=False",
                        "datePublished": "2021-04-02T18:53:05",
                    }
                ],
            },
            {
                "id": "175677",
                "title": "voorschot",
                "datePublished": "2021-04-04T18:53:05",
                "documents": [
                    {
                        "id": "660000000000471",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/aanvraag/document?id=660000000000471&isBulk=False&isDms=False",
                        "datePublished": "2021-04-04T18:53:05",
                    }
                ],
                "decision": "toekenning",
            },
            {
                "id": "175654",
                "title": "besluit",
                "datePublished": "2021-04-06T18:53:05",
                "documents": [
                    {
                        "id": "660000000000472",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/aanvraag/document?id=660000000000472&isBulk=False&isDms=False",
                        "datePublished": "2021-04-06T18:53:05",
                    }
                ],
                "decision": "toekenning",
            },
            {
                "id": "175651",
                "title": "besluit",
                "datePublished": "2021-04-08T18:53:05",
                "documents": [
                    {
                        "id": "660000000000473",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/aanvraag/document?id=660000000000473&isBulk=False&isDms=False",
                        "datePublished": "2021-04-08T18:53:05",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "bb17f3779128ae1745ad022fe6a6c1a9",
        "title": "Tozo 5 (aangevraagd vanaf 1 juli 2021)",
        "dateStart": "2021-07-02T18:53:05",
        "datePublished": "2021-07-08T18:53:05",
        "dateEnd": "2021-07-08T18:53:05",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "837",
                "title": "aanvraag",
                "datePublished": "2021-07-02T18:53:05",
                "documents": [
                    {
                        "id": "4400000123",
                        "title": "Ontvangst- bevestiging Aanvraag\n2021-07-02T18:53:05",
                        "url": "/wpi/aanvraag/document?id=4400000123&isBulk=True&isDms=False",
                        "datePublished": "2021-07-02T18:53:05",
                    }
                ],
            },
            {
                "id": "176171",
                "title": "voorschot",
                "datePublished": "2021-07-04T18:53:05",
                "documents": [
                    {
                        "id": "660000000000053",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/aanvraag/document?id=660000000000053&isBulk=False&isDms=False",
                        "datePublished": "2021-07-04T18:53:05",
                    }
                ],
            },
            {
                "id": "176167",
                "title": "besluit",
                "datePublished": "2021-07-06T18:53:05",
                "documents": [
                    {
                        "id": "660000000000054",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/aanvraag/document?id=660000000000054&isBulk=False&isDms=False",
                        "datePublished": "2021-07-06T18:53:05",
                    }
                ],
                "decision": "toekenning",
            },
            {
                "id": "176165",
                "title": "besluit",
                "datePublished": "2021-07-08T18:53:05",
                "documents": [
                    {
                        "id": "660000000000055",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/aanvraag/document?id=660000000000055&isBulk=False&isDms=False",
                        "datePublished": "2021-07-08T18:53:05",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "d9c09acc579d10266ca390c0ea08c8ad",
        "title": "TONK",
        "dateStart": "2021-01-05T17:20:04",
        "datePublished": "2021-08-12T17:20:04",
        "dateEnd": "2021-08-12T17:20:04",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "802",
                "title": "aanvraag",
                "datePublished": "2021-01-05T17:20:04",
                "documents": [
                    {
                        "id": "4400000095",
                        "title": "Aanvraag TONK\n2021-01-05T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000095&isBulk=True&isDms=False",
                        "datePublished": "2021-01-05T17:20:04",
                    }
                ],
            },
            {
                "id": "176137",
                "title": "herstelTermijn",
                "datePublished": "2021-01-06T17:20:04",
                "documents": [
                    {
                        "id": "660000000000500",
                        "title": "Brief meer informatie",
                        "url": "/wpi/aanvraag/document?id=660000000000500&isBulk=False&isDms=False",
                        "datePublished": "2021-01-06T17:20:04",
                    }
                ],
            },
            {
                "id": "176146",
                "title": "besluit",
                "datePublished": "2021-01-07T17:20:04",
                "documents": [
                    {
                        "id": "660000000000501",
                        "title": "Besluit buiten behandeling",
                        "url": "/wpi/aanvraag/document?id=660000000000501&isBulk=False&isDms=False",
                        "datePublished": "2021-01-07T17:20:04",
                    }
                ],
                "decision": "buitenbehandeling",
            },
            {
                "id": "843",
                "title": "correctiemail",
                "datePublished": "2021-08-08T17:20:04",
                "documents": [
                    {
                        "id": "4400000132",
                        "title": "Mail verkeerde TONK-brief",
                        "url": "/wpi/aanvraag/document?id=4400000132&isBulk=True&isDms=False",
                        "datePublished": "2021-08-08T17:20:04",
                    }
                ],
            },
            {
                "id": "176182",
                "title": "besluit",
                "datePublished": "2021-08-10T17:20:04",
                "documents": [
                    {
                        "id": "660000000010184",
                        "title": "Besluit over verlenging",
                        "url": "/wpi/aanvraag/document?id=660000000010184&isBulk=False&isDms=False",
                        "datePublished": "2021-08-10T17:20:04",
                    }
                ],
                "decision": "toekenning",
            },
            {
                "id": "1726182",
                "title": "besluit",
                "datePublished": "2021-08-12T17:20:04",
                "documents": [
                    {
                        "id": "660000000010185",
                        "title": "Brief bevestiging weigering",
                        "url": "/wpi/aanvraag/document?id=660000000010185&isBulk=False&isDms=False",
                        "datePublished": "2021-08-12T17:20:04",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "6cbb95f98cb9d1cf2835781e3923f857",
        "title": "Bbz",
        "dateStart": "2021-09-01T17:20:04",
        "datePublished": "2021-09-15T17:20:04",
        "dateEnd": None,
        "decision": None,
        "status": "aanvraag",
        "steps": [
            {
                "id": "844",
                "title": "aanvraag",
                "datePublished": "2021-09-01T17:20:04",
                "documents": [
                    {
                        "id": "4400000146",
                        "title": "Aanvraag Bbz\n2021-09-01T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000146&isBulk=True&isDms=False",
                        "datePublished": "2021-09-01T17:20:04",
                    },
                    {
                        "id": "4400000147",
                        "title": "Aanvraag Bbz\n2021-09-15T17:20:04",
                        "url": "/wpi/aanvraag/document?id=4400000147&isBulk=True&isDms=False",
                        "datePublished": "2021-09-15T17:20:04",
                    },
                ],
            },
            {
                "id": "175855",
                "title": "beslistermijn",
                "datePublished": "2021-09-02T17:20:04",
                "documents": [
                    {
                        "id": "660000000010211",
                        "title": "Brief verlenging beslistermijn",
                        "url": "/wpi/aanvraag/document?id=660000000010211&isBulk=False&isDms=False",
                        "datePublished": "2021-09-02T17:20:04",
                    }
                ],
            },
        ],
    },
    {
        "id": "8b6ea52ea4d163770993a16c1d66aec4",
        "title": "Ioaz",
        "dateStart": "2021-09-16T17:20:04",
        "datePublished": "2021-09-16T17:20:04",
        "dateEnd": None,
        "decision": None,
        "status": "herstelTermijn",
        "steps": [
            {
                "id": "176322",
                "title": "herstelTermijn",
                "datePublished": "2021-09-16T17:20:04",
                "documents": [
                    {
                        "id": "660000000010212",
                        "title": "Brief verzoek om meer informatie",
                        "url": "/wpi/aanvraag/document?id=660000000010212&isBulk=False&isDms=False",
                        "datePublished": "2021-09-16T17:20:04",
                    }
                ],
            }
        ],
    },
]
