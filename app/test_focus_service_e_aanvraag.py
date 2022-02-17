import datetime
import json
from textwrap import indent
from unittest import TestCase
from unittest.mock import call, patch

from app.focus_service_e_aanvraag import (
    create_e_aanvraag,
    get_document_config,
    get_e_aanvraag_step,
    get_e_aanvragen,
    get_steps_collection,
)
from app.test_app import MockClient


class FocusSerivceEAanvraag(TestCase):
    maxDiff = None

    def test_get_document_config(self):
        document_code_id = 176182
        document_config = get_document_config(document_code_id)

        self.assertEqual(document_config["product"], "tonk")
        self.assertEqual(document_config["step_id"], "besluit")
        self.assertEqual(document_config["decision"], "mogelijkeVerlenging")

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
                "id": "aanvraag",
                "datePublished": datetime.datetime(2020, 10, 23, 17, 20, 4),
                "title": "Aanvraag",
                "documents": [],
            }
        ]
        result_expected = {
            "title": "tozo 5",
            "id": "d7263e1172ef87e1a570f8cf1710b29a",
            "dateStart": "2020-10-23T17:20:04",
            "datePublished": "2020-10-23T17:20:04",
            "dateEnd": None,
            "decision": None,
            "status": "aanvraag",
            "steps": [
                {
                    "id": "aanvraag",
                    "title": "Aanvraag",
                    "datePublished": "2020-10-23T17:20:04",
                    "documents": [],
                }
            ],
        }
        result = create_e_aanvraag(product_name, steps)
        self.assertEqual(result, result_expected)

    def test_create_e_aanvraag2(self):
        product_name = "tonk"
        steps = [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": datetime.datetime(2020, 10, 23, 17, 20, 4),
                "documents": [],
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": datetime.datetime(2020, 11, 15, 10, 00, 2),
                "documents": [],
                "decision": "toekenning",
            },
        ]
        result_expected = {
            "title": "tonk",
            "id": "35243ffdb3668fc3f4607e7c41dea31e",
            "dateStart": "2020-10-23T17:20:04",
            "datePublished": "2020-11-15T10:00:02",
            "dateEnd": "2020-11-15T10:00:02",
            "decision": "toekenning",
            "status": "besluit",
            "steps": [
                {
                    "id": "aanvraag",
                    "title": "Aanvraag document",
                    "datePublished": "2020-10-23T17:20:04",
                    "title": "Aanvraag",
                    "documents": [],
                },
                {
                    "id": "besluit",
                    "title": "Besluit document",
                    "datePublished": "2020-11-15T10:00:02",
                    "title": "Besluit",
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
                "documentCode": "5364",
                "documentCodeId": "175364",
                "documentOmschrijving": "Tozo3 Afwijzen",
            },
            "documentId": 660000000000099,
            "isBulk": False,
            "isDms": False,
            "variant": None,
        }

        document_config = {
            "omschrijving": "Tozo3 Afwijzen",
            "step_id": "besluit",
            "product": "Tozo 3",
            "document_title": "Besluit afwijzing",
            "decision": "afwijzing",
        }

        result_expected = {
            "id": "besluit",
            "title": "Besluit",
            "datePublished": datetime.datetime(2020, 10, 27, 17, 20, 4),
            "decision": "afwijzing",
            "documents": [
                {
                    "id": "660000000000099",
                    "dceId": "175364",
                    "title": "Besluit afwijzing",
                    "datePublished": "2020-10-27T17:20:04",
                    "url": "/wpi/document?id=660000000000099&isBulk=False&isDms=False",
                }
            ],
        }

        result = get_e_aanvraag_step(e_aanvraag, document_config)

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
        "title": "tozo 1",
        "dateStart": "2020-03-27T17:20:04",
        "datePublished": "2020-04-08T17:20:04",
        "dateEnd": "2020-04-08T17:20:04",
        "decision": "toekenning",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": "2020-03-27T17:20:04",
                "documents": [
                    {
                        "id": "4400000027",
                        "dceId": "770",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-03-27T17:20:04",
                        "url": "/wpi/document?id=4400000027&isBulk=True&isDms=False",
                        "datePublished": "2020-03-27T17:20:04",
                    },
                    {
                        "id": "4400000034",
                        "dceId": "770",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-04-01T17:20:04",
                        "url": "/wpi/document?id=4400000034&isBulk=True&isDms=False",
                        "datePublished": "2020-04-01T17:20:04",
                    },
                    {
                        "id": "4400000033",
                        "dceId": "770",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-04-02T17:20:04",
                        "url": "/wpi/document?id=4400000033&isBulk=True&isDms=False",
                        "datePublished": "2020-04-02T17:20:04",
                    },
                ],
            },
            {
                "id": "voorschot",
                "title": "Voorschot",
                "datePublished": "2020-04-03T17:20:04",
                "documents": [
                    {
                        "id": "660000000000058",
                        "dceId": "175296",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000058&isBulk=False&isDms=False",
                        "datePublished": "2020-04-03T17:20:04",
                    }
                ],
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2020-04-08T17:20:04",
                "documents": [
                    {
                        "id": "660000000000059",
                        "dceId": "175303",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/document?id=660000000000059&isBulk=False&isDms=False",
                        "datePublished": "2020-04-08T17:20:04",
                    }
                ],
                "decision": "toekenning",
                "productSpecific": "uitkering",
            },
        ],
    },
    {
        "id": "ee5dc44e435040731d39b84e0fd0b4f5",
        "title": "tozo 2",
        "dateStart": "2020-06-19T17:20:04",
        "datePublished": "2020-07-04T17:20:04",
        "dateEnd": "2020-07-04T17:20:04",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": "2020-06-19T17:20:04",
                "documents": [
                    {
                        "id": "4400000071",
                        "dceId": "777",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-06-19T17:20:04",
                        "url": "/wpi/document?id=4400000071&isBulk=True&isDms=False",
                        "datePublished": "2020-06-19T17:20:04",
                    }
                ],
            },
            {
                "id": "voorschot",
                "title": "Voorschot",
                "datePublished": "2020-06-23T17:20:04",
                "documents": [
                    {
                        "id": "660000000000413",
                        "dceId": "175345",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000413&isBulk=False&isDms=False",
                        "datePublished": "2020-06-23T17:20:04",
                    }
                ],
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2020-07-03T17:20:04",
                "documents": [
                    {
                        "id": "660000000000076",
                        "dceId": "175336",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/document?id=660000000000076&isBulk=False&isDms=False",
                        "datePublished": "2020-07-03T17:20:04",
                    }
                ],
                "decision": "toekenning",
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2020-07-04T17:20:04",
                "documents": [
                    {
                        "id": "660000000000077",
                        "dceId": "175337",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/document?id=660000000000077&isBulk=False&isDms=False",
                        "datePublished": "2020-07-04T17:20:04",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "27c726a8ee4dd93a48c9f3c30cf865b2",
        "title": "tozo 3",
        "dateStart": "2020-10-14T17:20:04",
        "datePublished": "2020-10-27T17:20:04",
        "dateEnd": "2020-10-27T17:20:04",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": "2020-10-14T17:20:04",
                "documents": [
                    {
                        "id": "4400000053",
                        "dceId": "785",
                        "title": "Ontvangst- bevestiging Aanvraag\n2020-10-14T17:20:04",
                        "url": "/wpi/document?id=4400000053&isBulk=True&isDms=False",
                        "datePublished": "2020-10-14T17:20:04",
                    }
                ],
            },
            {
                "id": "voorschot",
                "title": "Voorschot",
                "datePublished": "2020-10-19T17:20:04",
                "documents": [
                    {
                        "id": "660000000000097",
                        "dceId": "175372",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000097&isBulk=False&isDms=False",
                        "datePublished": "2020-10-19T17:20:04",
                    }
                ],
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2020-10-23T17:20:04",
                "documents": [
                    {
                        "id": "660000000000098",
                        "dceId": "175309",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/document?id=660000000000098&isBulk=False&isDms=False",
                        "datePublished": "2020-10-23T17:20:04",
                    }
                ],
                "decision": "toekenning",
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2020-10-27T17:20:04",
                "documents": [
                    {
                        "id": "660000000000099",
                        "dceId": "175364",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/document?id=660000000000099&isBulk=False&isDms=False",
                        "datePublished": "2020-10-27T17:20:04",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "e9fabddf1d6e9386622faeba4c945c48",
        "title": "tozo 4",
        "dateStart": "2021-04-02T18:53:05",
        "datePublished": "2021-04-08T18:53:05",
        "dateEnd": "2021-04-08T18:53:05",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": "2021-04-02T18:53:05",
                "documents": [
                    {
                        "id": "4400000022",
                        "dceId": "800",
                        "title": "Ontvangst- bevestiging Aanvraag\n2021-04-02T18:53:05",
                        "url": "/wpi/document?id=4400000022&isBulk=True&isDms=False",
                        "datePublished": "2021-04-02T18:53:05",
                    }
                ],
            },
            {
                "id": "voorschot",
                "title": "Voorschot",
                "datePublished": "2021-04-04T18:53:05",
                "documents": [
                    {
                        "id": "660000000000471",
                        "dceId": "175677",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000471&isBulk=False&isDms=False",
                        "datePublished": "2021-04-04T18:53:05",
                    }
                ],
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2021-04-06T18:53:05",
                "documents": [
                    {
                        "id": "660000000000472",
                        "dceId": "175654",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/document?id=660000000000472&isBulk=False&isDms=False",
                        "datePublished": "2021-04-06T18:53:05",
                    }
                ],
                "decision": "toekenning",
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2021-04-08T18:53:05",
                "documents": [
                    {
                        "id": "660000000000473",
                        "dceId": "175651",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/document?id=660000000000473&isBulk=False&isDms=False",
                        "datePublished": "2021-04-08T18:53:05",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "bb17f3779128ae1745ad022fe6a6c1a9",
        "title": "tozo 5",
        "dateStart": "2021-07-02T18:53:05",
        "datePublished": "2021-07-08T18:53:05",
        "dateEnd": "2021-07-08T18:53:05",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": "2021-07-02T18:53:05",
                "documents": [
                    {
                        "id": "4400000123",
                        "dceId": "837",
                        "title": "Ontvangst- bevestiging Aanvraag\n2021-07-02T18:53:05",
                        "url": "/wpi/document?id=4400000123&isBulk=True&isDms=False",
                        "datePublished": "2021-07-02T18:53:05",
                    }
                ],
            },
            {
                "id": "voorschot",
                "title": "Voorschot",
                "datePublished": "2021-07-04T18:53:05",
                "documents": [
                    {
                        "id": "660000000000053",
                        "dceId": "176171",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000053&isBulk=False&isDms=False",
                        "datePublished": "2021-07-04T18:53:05",
                    }
                ],
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2021-07-06T18:53:05",
                "documents": [
                    {
                        "id": "660000000000054",
                        "dceId": "176167",
                        "title": "Besluit toekenning uitkering",
                        "url": "/wpi/document?id=660000000000054&isBulk=False&isDms=False",
                        "datePublished": "2021-07-06T18:53:05",
                    }
                ],
                "decision": "toekenning",
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2021-07-08T18:53:05",
                "documents": [
                    {
                        "id": "660000000000055",
                        "dceId": "176165",
                        "title": "Besluit afwijzing",
                        "url": "/wpi/document?id=660000000000055&isBulk=False&isDms=False",
                        "datePublished": "2021-07-08T18:53:05",
                    }
                ],
                "decision": "afwijzing",
            },
        ],
    },
    {
        "id": "d9c09acc579d10266ca390c0ea08c8ad",
        "title": "tonk",
        "dateStart": "2021-01-05T17:20:04",
        "datePublished": "2021-08-12T17:20:04",
        "dateEnd": "2021-08-10T17:20:04",
        "decision": "mogelijkeVerlenging",
        "status": "briefWeigering",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": "2021-01-05T17:20:04",
                "documents": [
                    {
                        "id": "4400000095",
                        "dceId": "802",
                        "title": "Aanvraag TONK\n2021-01-05T17:20:04",
                        "url": "/wpi/document?id=4400000095&isBulk=True&isDms=False",
                        "datePublished": "2021-01-05T17:20:04",
                    }
                ],
                "productSpecific": "uitkering",
            },
            {
                "id": "herstelTermijn",
                "title": "Informatie nodig",
                "datePublished": "2021-01-06T17:20:04",
                "documents": [
                    {
                        "id": "660000000000500",
                        "dceId": "176137",
                        "title": "Brief meer informatie",
                        "url": "/wpi/document?id=660000000000500&isBulk=False&isDms=False",
                        "datePublished": "2021-01-06T17:20:04",
                    }
                ],
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2021-01-07T17:20:04",
                "documents": [
                    {
                        "id": "660000000000501",
                        "dceId": "176146",
                        "title": "Besluit buiten behandeling",
                        "url": "/wpi/document?id=660000000000501&isBulk=False&isDms=False",
                        "datePublished": "2021-01-07T17:20:04",
                    }
                ],
                "decision": "buitenBehandeling",
                "productSpecific": "uitkering",
            },
            {
                "id": "correctiemail",
                "title": "Mail",
                "datePublished": "2021-08-08T17:20:04",
                "documents": [
                    {
                        "id": "4400000132",
                        "dceId": "843",
                        "title": "Mail verkeerde TONK-brief",
                        "url": "/wpi/document?id=4400000132&isBulk=True&isDms=False",
                        "datePublished": "2021-08-08T17:20:04",
                    }
                ],
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "title": "Besluit",
                "datePublished": "2021-08-10T17:20:04",
                "documents": [
                    {
                        "id": "660000000010184",
                        "dceId": "176182",
                        "title": "Besluit over verlenging",
                        "url": "/wpi/document?id=660000000010184&isBulk=False&isDms=False",
                        "datePublished": "2021-08-10T17:20:04",
                    }
                ],
                "decision": "mogelijkeVerlenging",
                "productSpecific": "uitkering",
            },
            {
                "id": "briefWeigering",
                "title": "Brief",
                "datePublished": "2021-08-12T17:20:04",
                "documents": [
                    {
                        "id": "660000000010185",
                        "dceId": "1726182",
                        "title": "Brief bevestiging weigering",
                        "url": "/wpi/document?id=660000000010185&isBulk=False&isDms=False",
                        "datePublished": "2021-08-12T17:20:04",
                    }
                ],
                "productSpecific": "uitkering",
            },
        ],
    },
    {
        "id": "6cbb95f98cb9d1cf2835781e3923f857",
        "title": "bbz",
        "dateStart": "2021-09-01T17:20:04",
        "datePublished": "2021-09-15T17:20:04",
        "dateEnd": None,
        "decision": None,
        "status": "aanvraag",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "datePublished": "2021-09-01T17:20:04",
                "documents": [
                    {
                        "id": "4400000146",
                        "dceId": "844",
                        "title": "Aanvraag Bbz\n2021-09-01T17:20:04",
                        "url": "/wpi/document?id=4400000146&isBulk=True&isDms=False",
                        "datePublished": "2021-09-01T17:20:04",
                    },
                    {
                        "id": "4400000147",
                        "dceId": "844",
                        "title": "Aanvraag Bbz\n2021-09-15T17:20:04",
                        "url": "/wpi/document?id=4400000147&isBulk=True&isDms=False",
                        "datePublished": "2021-09-15T17:20:04",
                    },
                ],
            },
            {
                "id": "beslisTermijn",
                "title": "Tijd nodig",
                "datePublished": "2021-09-02T17:20:04",
                "documents": [
                    {
                        "id": "660000000010211",
                        "dceId": "175855",
                        "title": "Brief verlenging beslistermijn",
                        "url": "/wpi/document?id=660000000010211&isBulk=False&isDms=False",
                        "datePublished": "2021-09-02T17:20:04",
                    }
                ],
            },
        ],
    },
    {
        "id": "8b6ea52ea4d163770993a16c1d66aec4",
        "title": "ioaz",
        "dateStart": "2021-09-16T17:20:04",
        "datePublished": "2021-09-16T17:20:04",
        "dateEnd": None,
        "decision": None,
        "status": "herstelTermijn",
        "steps": [
            {
                "id": "herstelTermijn",
                "title": "Informatie nodig",
                "datePublished": "2021-09-16T17:20:04",
                "documents": [
                    {
                        "id": "660000000010212",
                        "dceId": "176322",
                        "title": "Brief verzoek om meer informatie",
                        "url": "/wpi/document?id=660000000010212&isBulk=False&isDms=False",
                        "datePublished": "2021-09-16T17:20:04",
                    }
                ],
            }
        ],
    },
]
