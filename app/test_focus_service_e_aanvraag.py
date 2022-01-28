import datetime
from unittest import TestCase
from unittest.mock import patch

from app.focus_service_e_aanvraag import (
    create_e_aanvraag,
    get_document_config,
    get_e_aanvraag_step,
    get_e_aanvragen,
    get_steps_collection,
)


class FocusSerivceEAanvraag(TestCase):
    maxDiff = None

    def test_get_document_config(self):
        document_code_id = 176182
        document_config = get_document_config(document_code_id)

        self.assertEqual(document_config["product"], "tonk")
        self.assertEqual(document_config["stepType"], "besluit")
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
            },
        )

    @patch("app.focus_service_aanvragen.get_document_url")
    def test_create_e_aanvraag(self, get_document_url_mock):
        get_document_url_mock.return_value = "http://ho/ho/ho"

        product_name = "tozo 5"
        steps = [
            {
                "id": "1x1",
                "title": "Aanvraag document",
                "url": "http://ho/ho/ho",
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
                    "url": "http://ho/ho/ho",
                    "datePublished": "2020-10-23T17:20:04",
                    "status": "aanvraag",
                    "documents": [],
                }
            ],
        }
        result = create_e_aanvraag(product_name, steps)
        self.assertEqual(result, result_expected)

    @patch("app.focus_service_aanvragen.get_document_url")
    def test_create_e_aanvraag(self, get_document_url_mock):
        get_document_url_mock.return_value = "http://ho/ho/ho"

        product_name = "tonk"
        steps = [
            {
                "id": "1x1",
                "title": "Aanvraag document",
                "url": "http://ho/ho/ho",
                "datePublished": datetime.datetime(2020, 10, 23, 17, 20, 4),
                "status": "aanvraag",
                "documents": [],
            },
            {
                "id": "1x2",
                "title": "Besluit document",
                "url": "http://ho/ho/ho",
                "datePublished": datetime.datetime(2020, 11, 15, 10, 00, 2),
                "status": "besluit",
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
                    "url": "http://ho/ho/ho",
                    "datePublished": "2020-10-23T17:20:04",
                    "status": "aanvraag",
                    "documents": [],
                },
                {
                    "id": "1x2",
                    "title": "Besluit document",
                    "url": "http://ho/ho/ho",
                    "datePublished": "2020-11-15T10:00:02",
                    "status": "besluit",
                    "decision": "toekenning",
                    "documents": [],
                },
            ],
        }
        result = create_e_aanvraag(product_name, steps)
        self.assertEqual(result, result_expected)

    # def test_get_e_aanvraag_step(self):
    #     e_aanvraag = {}
    #     document_code_id = ""
    #     document_config = {}
    #     result = get_e_aanvraag_step(e_aanvraag, document_code_id, document_config)
    #     self.assertEqual(result)

    # def test_get_e_aanvragen(self):
    #     bsn = ""
    #     result = get_e_aanvragen(bsn)
    #     self.assertEqual(result)


example_response = {
    "bsn": 307741837,
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
