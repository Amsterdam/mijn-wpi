import datetime
import json
from unittest.mock import MagicMock, patch
from app.config import CustomJSONEncoder
from app.focus_service import get_aanvragen
from tests.focus_test_app import FocusApiTestApp


class MockService:
    getAanvragen = MagicMock()


class MockClient:
    def __init__(self, get_aanvragen_response) -> None:
        service = MockService()
        service.getAanvragen.return_value = get_aanvragen_response
        self.service = service


def create_soap_response(soort_product_naam, product, bsn=12312312399):
    return {
        "bsn": bsn,
        "soortProduct": [{"naam": soort_product_naam, "product": [product]}],
    }


class TestFocusBijstandAanvraag(FocusApiTestApp):

    bsn = 12312312399
    product_source = {
        "dienstverleningstermijn": 21,
        "inspanningsperiode": 28,
        "naam": "Levensonderhoud",
        "processtappen": {
            "aanvraag": {
                "datum": datetime.datetime(2017, 8, 17, 15, 5, 52),
                "document": [],
            },
            "beslissing": {
                "datum": datetime.datetime(2017, 8, 21, 15, 5, 52),
                "document": [],
                "reden": "Weet ik veel",
            },
            "bezwaar": None,
            "herstelTermijn": {
                "datum": datetime.datetime(2017, 8, 18, 15, 5, 52),
                "document": [
                    {
                        "id": "4400000007",
                        "isBulk": True,
                        "isDms": False,
                        "omschrijving": "Formulier Inlichtingen Klant",
                    },
                    {
                        "id": "4400000010",
                        "isBulk": True,
                        "isDms": False,
                        "omschrijving": "Formulier Inlichtingen partner",
                    },
                    {
                        "id": "4400000008",
                        "isBulk": True,
                        "isDms": False,
                        "omschrijving": "Aanvraagformulier WWB (kort)",
                    },
                ],
                "aantalDagenHerstelTermijn": 10,
            },
            "inBehandeling": {
                "datum": datetime.datetime(2017, 8, 17, 15, 5, 52),
                "document": [],
            },
        },
        "typeBesluit": "Afwijzing",
    }
    product_transformed = {
        "id": "318055ab142430bcd6eda77c8b78fdab",
        "title": "Bijstandsuitkering",
        "status": "besluit",
        "decision": "afwijzing",
        "datePublished": "2017-08-21T15:05:52",
        "dateStart": "2017-08-17T15:05:52",
        "dateEnd": "2017-08-21T15:05:52",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "documents": [],
                "datePublished": "2017-08-17T15:05:52",
            },
            {
                "id": "inBehandeling",
                "title": "In behandeling",
                "documents": [],
                "datePublished": "2017-08-17T15:05:52",
                "dateDecisionExpected": "2017-10-05T15:05:52",
            },
            {
                "id": "herstelTermijn",
                "title": "Informatie nodig",
                "documents": {
                    "id": "4400000007",
                    "title": "Formulier Inlichtingen Klant",
                    "url": "/focus/document?id=4400000007&isBulk=True&isDms=False",
                    "datePublished": "2017-08-18T15:05:52",
                    "type": "pdf",
                },
                "datePublished": "2017-08-18T15:05:52",
                "dateDecisionExpected": "2017-10-15T15:05:52",
                "dateUserFeedbackExpected": "2017-08-27T15:05:52",
            },
            {
                "id": "besluit",
                "title": "beslissing",
                "documents": [],
                "datePublished": "2017-08-21T15:05:52",
                "decision": "Afwijzing",
            },
        ],
    }

    @patch("app.focus_service.get_client")
    def test_get_aanvraag(self, get_client_mock):
        mock_client = MockClient(
            get_aanvragen_response=create_soap_response(
                "Participatiewet", self.product_source
            )
        )
        get_client_mock.return_value = mock_client
        response = get_aanvragen(bsn=self.bsn)

        self.assertTrue(len(response) == 1)
        mock_client.service.getAanvragen.assert_called_with(self.bsn)

        product = response[0]
        self.assertEqual(product, self.product_transformed)


class TestFocusStadspasAanvraag(FocusApiTestApp):

    bsn = 12312312399
    product_source = {
        "dienstverleningstermijn": 56,
        "inspanningsperiode": None,
        "naam": "Stadspas",
        "processtappen": {
            "aanvraag": {
                "datum": datetime.datetime(2019, 5, 8, 15, 5, 52),
                "document": [
                    {
                        "id": "4400000013",
                        "isBulk": True,
                        "isDms": False,
                        "omschrijving": "Aanvraag Stadspas (balie)",
                    }
                ],
            },
            "beslissing": {
                "datum": datetime.datetime(2019, 6, 7, 15, 5, 52),
                "document": [],
                "reden": None,
            },
            "bezwaar": None,
            "herstelTermijn": {
                "datum": datetime.datetime(2019, 5, 17, 15, 5, 52),
                "document": [],
                "aantalDagenHerstelTermijn": 20,
            },
            "inBehandeling": {
                "datum": datetime.datetime(2019, 5, 10, 15, 5, 52),
                "document": [],
            },
        },
        "typeBesluit": "Toekenning",
    }
    product_transformed = {
        "id": "4b46c9865ac4f007b2b0fdd03fd1fbba",
        "title": "Stadspas",
        "status": "besluit",
        "decision": "toekenning",
        "datePublished": "2019-06-07T15:05:52",
        "dateStart": "2019-05-08T15:05:52",
        "dateEnd": "2019-06-07T15:05:52",
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "documents": {
                    "id": "4400000013",
                    "title": "Aanvraag Stadspas (balie)",
                    "url": "/focus/document?id=4400000013&isBulk=True&isDms=False",
                    "datePublished": "2019-05-08T15:05:52",
                    "type": "pdf",
                },
                "datePublished": "2019-05-08T15:05:52",
            },
            {
                "id": "inBehandeling",
                "title": "In behandeling",
                "documents": [],
                "datePublished": "2019-05-10T15:05:52",
                "dateDecisionExpected": "2019-07-03T15:05:52",
            },
            {
                "id": "herstelTermijn",
                "title": "Informatie nodig",
                "documents": [],
                "datePublished": "2019-05-17T15:05:52",
                "dateDecisionExpected": "2019-07-23T15:05:52",
                "dateUserFeedbackExpected": "2019-05-28T15:05:52",
            },
            {
                "id": "besluit",
                "title": "beslissing",
                "documents": [],
                "datePublished": "2019-06-07T15:05:52",
                "decision": "Toekenning",
            },
        ],
    }

    @patch("app.focus_service.get_client")
    def test_get_aanvraag(self, get_client_mock):
        mock_client = MockClient(
            get_aanvragen_response=create_soap_response(
                "Minimafonds", self.product_source
            )
        )
        get_client_mock.return_value = mock_client
        response = get_aanvragen(bsn=self.bsn)

        self.assertTrue(len(response) == 1)
        mock_client.service.getAanvragen.assert_called_with(self.bsn)

        product = response[0]
        self.assertEqual(product, self.product_transformed)
