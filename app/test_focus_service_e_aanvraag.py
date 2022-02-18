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


class FocusServiceEAanvraag(TestCase):
    maxDiff = None

    def test_get_document_config(self):
        document_code_id = 176182
        document_config = get_document_config(document_code_id)

        self.assertEqual(document_config["about"], "TONK")
        self.assertEqual(document_config["step_id"], "besluit")
        self.assertEqual(document_config["decision"], "mogelijkeVerlenging")

        document_config = get_document_config(123)

        self.assertIsNone(document_config)

    def test_get_steps_collection(self):
        collection = get_steps_collection()
        self.assertEqual(
            collection,
            {
                "Tozo 1": [],
                "Tozo 2": [],
                "Tozo 3": [],
                "Tozo 4": [],
                "Tozo 5": [],
                "TONK": [],
                "Bbz": [],
            },
        )

    def test_create_e_aanvraag(self):

        product_name = "Tozo 5"
        steps = [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": datetime.datetime(2020, 10, 23, 17, 20, 4),
                "documents": [],
            }
        ]
        result_expected = {
            "title": "Tozo 5 (aangevraagd vanaf 1 juli 2021)",
            "about": "Tozo 5",
            "id": "8c04fe509fe8e9e817807e85d639810b",
            "dateStart": "2020-10-23T17:20:04",
            "datePublished": "2020-10-23T17:20:04",
            "dateEnd": None,
            "decision": None,
            "status": "aanvraag",
            "steps": [
                {
                    "id": "aanvraag",
                    "status": "Aanvraag",
                    "datePublished": "2020-10-23T17:20:04",
                    "documents": [],
                }
            ],
        }
        result = create_e_aanvraag(product_name, steps)
        self.assertEqual(result, result_expected)

    def test_create_e_aanvraag2(self):
        product_name = "TONK"
        steps = [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": datetime.datetime(2020, 10, 23, 17, 20, 4),
                "documents": [],
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": datetime.datetime(2020, 11, 15, 10, 00, 2),
                "documents": [],
                "decision": "toekenning",
            },
        ]
        result_expected = {
            "title": "TONK",
            "about": "TONK",
            "id": "d818f43f721dddca7dce630d1e9ac940",
            "dateStart": "2020-10-23T17:20:04",
            "datePublished": "2020-11-15T10:00:02",
            "dateEnd": "2020-11-15T10:00:02",
            "decision": "toekenning",
            "status": "besluit",
            "steps": [
                {
                    "id": "aanvraag",
                    "datePublished": "2020-10-23T17:20:04",
                    "status": "Aanvraag",
                    "documents": [],
                },
                {
                    "id": "besluit",
                    "datePublished": "2020-11-15T10:00:02",
                    "status": "Besluit",
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
            "about": "Tozo 3",
            "step_id": "besluit",
            "document_title": "Besluit afwijzing",
            "decision": "afwijzing",
        }

        result_expected = {
            "id": "besluit",
            "status": "Besluit",
            "datePublished": datetime.datetime(2020, 10, 27, 17, 20, 4),
            "decision": "afwijzing",
            "documents": [
                {
                    "id": "660000000000099",
                    "dcteId": "175364",
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
            response=example_soap_response, name="getEAanvraagTOZO"
        )
        get_client_mock.return_value = mock_client
        bsn = "123xx123"
        result = get_e_aanvragen(bsn)
        # print(json.dumps(result, indent=4))

        mock_client.service.getEAanvraagTOZO.assert_called_with(bsn)
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
        "id": "6c31bbf416232a8b9b1240257b358ed6",
        "title": "Tozo 1 (aangevraagd voor 1 juni 2020)",
        "about": "Tozo 1",
        "dateStart": "2020-03-27T17:20:04",
        "datePublished": "2020-04-08T17:20:04",
        "dateEnd": "2020-04-08T17:20:04",
        "decision": "toekenning",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": "2020-03-27T17:20:04",
                "documents": [
                    {
                        "id": "4400000027",
                        "dcteId": "770",
                        "title": "Aanvraag Tozo 1\n27 maart 2020 17:20",
                        "url": "/wpi/document?id=4400000027&isBulk=True&isDms=False",
                        "datePublished": "2020-03-27T17:20:04",
                    },
                    {
                        "id": "4400000034",
                        "dcteId": "770",
                        "title": "Aanvraag Tozo 1\n01 april 2020 17:20",
                        "url": "/wpi/document?id=4400000034&isBulk=True&isDms=False",
                        "datePublished": "2020-04-01T17:20:04",
                    },
                    {
                        "id": "4400000033",
                        "dcteId": "770",
                        "title": "Aanvraag Tozo 1\n02 april 2020 17:20",
                        "url": "/wpi/document?id=4400000033&isBulk=True&isDms=False",
                        "datePublished": "2020-04-02T17:20:04",
                    },
                ],
            },
            {
                "id": "voorschot",
                "status": "Voorschot",
                "datePublished": "2020-04-03T17:20:04",
                "documents": [
                    {
                        "id": "660000000000058",
                        "dcteId": "175296",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000058&isBulk=False&isDms=False",
                        "datePublished": "2020-04-03T17:20:04",
                    }
                ],
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": "2020-04-08T17:20:04",
                "documents": [
                    {
                        "id": "660000000000059",
                        "dcteId": "175303",
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
        "id": "61d58ab37ffe556198d625b947e90b1a",
        "title": "Tozo 2 (aangevraagd vanaf 1 juni 2020)",
        "about": "Tozo 2",
        "dateStart": "2020-06-19T17:20:04",
        "datePublished": "2020-07-04T17:20:04",
        "dateEnd": "2020-07-04T17:20:04",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": "2020-06-19T17:20:04",
                "documents": [
                    {
                        "id": "4400000071",
                        "dcteId": "777",
                        "title": "Aanvraag Tozo 2\n19 juni 2020 17:20",
                        "url": "/wpi/document?id=4400000071&isBulk=True&isDms=False",
                        "datePublished": "2020-06-19T17:20:04",
                    }
                ],
            },
            {
                "id": "voorschot",
                "status": "Voorschot",
                "datePublished": "2020-06-23T17:20:04",
                "documents": [
                    {
                        "id": "660000000000413",
                        "dcteId": "175345",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000413&isBulk=False&isDms=False",
                        "datePublished": "2020-06-23T17:20:04",
                    }
                ],
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": "2020-07-03T17:20:04",
                "documents": [
                    {
                        "id": "660000000000076",
                        "dcteId": "175336",
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
                "status": "Besluit",
                "datePublished": "2020-07-04T17:20:04",
                "documents": [
                    {
                        "id": "660000000000077",
                        "dcteId": "175337",
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
        "id": "b01879e9ea8233e8c7008d0978279613",
        "title": "Tozo 3 (aangevraagd vanaf 1 oktober 2020)",
        "about": "Tozo 3",
        "dateStart": "2020-10-14T17:20:04",
        "datePublished": "2020-10-27T17:20:04",
        "dateEnd": "2020-10-27T17:20:04",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": "2020-10-14T17:20:04",
                "documents": [
                    {
                        "id": "4400000053",
                        "dcteId": "785",
                        "title": "Aanvraag Tozo 3\n14 oktober 2020 17:20",
                        "url": "/wpi/document?id=4400000053&isBulk=True&isDms=False",
                        "datePublished": "2020-10-14T17:20:04",
                    }
                ],
            },
            {
                "id": "voorschot",
                "status": "Voorschot",
                "datePublished": "2020-10-19T17:20:04",
                "documents": [
                    {
                        "id": "660000000000097",
                        "dcteId": "175372",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000097&isBulk=False&isDms=False",
                        "datePublished": "2020-10-19T17:20:04",
                    }
                ],
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": "2020-10-23T17:20:04",
                "documents": [
                    {
                        "id": "660000000000098",
                        "dcteId": "175309",
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
                "status": "Besluit",
                "datePublished": "2020-10-27T17:20:04",
                "documents": [
                    {
                        "id": "660000000000099",
                        "dcteId": "175364",
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
        "id": "0c4133dba3fe3d0d6b11f31ecd860382",
        "title": "Tozo 4 (aangevraagd vanaf 1 april 2021)",
        "about": "Tozo 4",
        "dateStart": "2021-04-02T18:53:05",
        "datePublished": "2021-04-08T18:53:05",
        "dateEnd": "2021-04-08T18:53:05",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": "2021-04-02T18:53:05",
                "documents": [
                    {
                        "id": "4400000022",
                        "dcteId": "800",
                        "title": "Aanvraag Tozo 4\n02 april 2021 18:53",
                        "url": "/wpi/document?id=4400000022&isBulk=True&isDms=False",
                        "datePublished": "2021-04-02T18:53:05",
                    }
                ],
            },
            {
                "id": "voorschot",
                "status": "Voorschot",
                "datePublished": "2021-04-04T18:53:05",
                "documents": [
                    {
                        "id": "660000000000471",
                        "dcteId": "175677",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000471&isBulk=False&isDms=False",
                        "datePublished": "2021-04-04T18:53:05",
                    }
                ],
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": "2021-04-06T18:53:05",
                "documents": [
                    {
                        "id": "660000000000472",
                        "dcteId": "175654",
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
                "status": "Besluit",
                "datePublished": "2021-04-08T18:53:05",
                "documents": [
                    {
                        "id": "660000000000473",
                        "dcteId": "175651",
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
        "id": "6ac434393fa829c96750416707e1b8f0",
        "title": "Tozo 5 (aangevraagd vanaf 1 juli 2021)",
        "about": "Tozo 5",
        "dateStart": "2021-07-02T18:53:05",
        "datePublished": "2021-07-08T18:53:05",
        "dateEnd": "2021-07-08T18:53:05",
        "decision": "afwijzing",
        "status": "besluit",
        "steps": [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": "2021-07-02T18:53:05",
                "documents": [
                    {
                        "id": "4400000123",
                        "dcteId": "837",
                        "title": "Aanvraag Tozo 5\n02 juli 2021 18:53",
                        "url": "/wpi/document?id=4400000123&isBulk=True&isDms=False",
                        "datePublished": "2021-07-02T18:53:05",
                    }
                ],
            },
            {
                "id": "voorschot",
                "status": "Voorschot",
                "datePublished": "2021-07-04T18:53:05",
                "documents": [
                    {
                        "id": "660000000000053",
                        "dcteId": "176171",
                        "title": "Brief betaling voorschot",
                        "url": "/wpi/document?id=660000000000053&isBulk=False&isDms=False",
                        "datePublished": "2021-07-04T18:53:05",
                    }
                ],
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": "2021-07-06T18:53:05",
                "documents": [
                    {
                        "id": "660000000000054",
                        "dcteId": "176167",
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
                "status": "Besluit",
                "datePublished": "2021-07-08T18:53:05",
                "documents": [
                    {
                        "id": "660000000000055",
                        "dcteId": "176165",
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
        "id": "27ece36a035186e3c7863e03554a6c2e",
        "title": "TONK",
        "about": "TONK",
        "dateStart": "2021-01-05T17:20:04",
        "datePublished": "2021-08-12T17:20:04",
        "dateEnd": "2021-08-10T17:20:04",
        "decision": "mogelijkeVerlenging",
        "status": "briefWeigering",
        "steps": [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": "2021-01-05T17:20:04",
                "documents": [
                    {
                        "id": "4400000095",
                        "dcteId": "802",
                        "title": "Aanvraag TONK\n05 januari 2021 17:20",
                        "url": "/wpi/document?id=4400000095&isBulk=True&isDms=False",
                        "datePublished": "2021-01-05T17:20:04",
                    }
                ],
                "productSpecific": "uitkering",
            },
            {
                "id": "herstelTermijn",
                "status": "Informatie nodig",
                "datePublished": "2021-01-06T17:20:04",
                "documents": [
                    {
                        "id": "660000000000500",
                        "dcteId": "176137",
                        "title": "Brief meer informatie",
                        "url": "/wpi/document?id=660000000000500&isBulk=False&isDms=False",
                        "datePublished": "2021-01-06T17:20:04",
                    }
                ],
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": "2021-01-07T17:20:04",
                "documents": [
                    {
                        "id": "660000000000501",
                        "dcteId": "176146",
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
                "status": "Mail",
                "datePublished": "2021-08-08T17:20:04",
                "documents": [
                    {
                        "id": "4400000132",
                        "dcteId": "843",
                        "title": "Mail verkeerde TONK-brief",
                        "url": "/wpi/document?id=4400000132&isBulk=True&isDms=False",
                        "datePublished": "2021-08-08T17:20:04",
                    }
                ],
                "productSpecific": "uitkering",
            },
            {
                "id": "besluit",
                "status": "Besluit",
                "datePublished": "2021-08-10T17:20:04",
                "documents": [
                    {
                        "id": "660000000010184",
                        "dcteId": "176182",
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
                "status": "Brief",
                "datePublished": "2021-08-12T17:20:04",
                "documents": [
                    {
                        "id": "660000000010185",
                        "dcteId": "1726182",
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
        "id": "899b4f4473a2692bc1a5558d5ab95f8c",
        "title": "Bbz",
        "about": "Bbz",
        "dateStart": "2021-09-01T17:20:04",
        "datePublished": "2021-09-16T17:20:04",
        "dateEnd": None,
        "decision": None,
        "status": "herstelTermijn",
        "steps": [
            {
                "id": "aanvraag",
                "status": "Aanvraag",
                "datePublished": "2021-09-01T17:20:04",
                "documents": [
                    {
                        "id": "4400000146",
                        "dcteId": "844",
                        "title": "Aanvraag Bbz\n01 september 2021 17:20",
                        "url": "/wpi/document?id=4400000146&isBulk=True&isDms=False",
                        "datePublished": "2021-09-01T17:20:04",
                    },
                    {
                        "id": "4400000147",
                        "dcteId": "844",
                        "title": "Aanvraag Bbz\n15 september 2021 17:20",
                        "url": "/wpi/document?id=4400000147&isBulk=True&isDms=False",
                        "datePublished": "2021-09-15T17:20:04",
                    },
                ],
            },
            {
                "id": "beslisTermijn",
                "status": "Tijd nodig",
                "datePublished": "2021-09-02T17:20:04",
                "documents": [
                    {
                        "id": "660000000010211",
                        "dcteId": "175855",
                        "title": "Brief verlenging beslistermijn",
                        "url": "/wpi/document?id=660000000010211&isBulk=False&isDms=False",
                        "datePublished": "2021-09-02T17:20:04",
                    }
                ],
            },
            {
                "id": "herstelTermijn",
                "status": "Informatie nodig",
                "datePublished": "2021-09-16T17:20:04",
                "documents": [
                    {
                        "id": "660000000010212",
                        "dcteId": "176322",
                        "title": "Brief verzoek om meer informatie",
                        "url": "/wpi/document?id=660000000010212&isBulk=False&isDms=False",
                        "datePublished": "2021-09-16T17:20:04",
                    }
                ],
                "about": "IOAZ",
            },
        ],
    },
]
