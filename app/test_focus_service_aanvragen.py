import datetime
from unittest import TestCase
from unittest.mock import patch

from app.focus_service_aanvragen import (
    calculate_municipality_feedback_date_max,
    calculate_user_feedback_date_max,
    get_aanvragen,
    get_client,
    get_decision,
    get_document_url,
    get_step_title,
    get_translation,
)
from app.test_app import MockClient, WpiApiTestApp


def create_soap_response_get_aanvragen(soort_product_naam, product, bsn=12312312399):
    return {
        "bsn": bsn,
        "soortProduct": [{"naam": soort_product_naam, "product": [product]}],
    }


class TestFocusBijstandAanvraag(TestCase):

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
                "documents": [
                    {
                        "id": "4400000007",
                        "title": "Formulier Inlichtingen Klant",
                        "url": "/wpi/aanvraag/document?id=4400000007&isBulk=True&isDms=False",
                        "datePublished": "2017-08-18T15:05:52",
                    },
                    {
                        "id": "4400000010",
                        "title": "Formulier Inlichtingen partner",
                        "url": "/wpi/aanvraag/document?id=4400000010&isBulk=True&isDms=False",
                        "datePublished": "2017-08-18T15:05:52",
                    },
                    {
                        "id": "4400000008",
                        "title": "Aanvraagformulier WWB (kort)",
                        "url": "/wpi/aanvraag/document?id=4400000008&isBulk=True&isDms=False",
                        "datePublished": "2017-08-18T15:05:52",
                    },
                ],
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

    @patch("app.focus_service_aanvragen.get_client")
    def test_get_aanvraag(self, get_client_mock):
        mock_client = MockClient(
            name="getAanvragen",
            response=create_soap_response_get_aanvragen(
                "Participatiewet", self.product_source
            ),
        )
        get_client_mock.return_value = mock_client
        response = get_aanvragen(bsn=self.bsn)

        self.assertTrue(len(response) == 1)
        mock_client.service.getAanvragen.assert_called_with(self.bsn)

        product = response[0]
        self.assertEqual(product, self.product_transformed)


class TestFocusStadspasAanvraag(TestCase):

    bsn = 99321321321
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
                "documents": [
                    {
                        "id": "4400000013",
                        "title": "Aanvraag Stadspas (balie)",
                        "url": "/wpi/aanvraag/document?id=4400000013&isBulk=True&isDms=False",
                        "datePublished": "2019-05-08T15:05:52",
                    }
                ],
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

    @patch("app.focus_service_aanvragen.get_client")
    def test_get_aanvraag(self, get_client_mock):
        mock_client = MockClient(
            name="getAanvragen",
            response=create_soap_response_get_aanvragen(
                "Minimafonds", self.product_source
            ),
        )
        get_client_mock.return_value = mock_client
        response = get_aanvragen(bsn=self.bsn)

        self.assertTrue(len(response) == 1)
        mock_client.service.getAanvragen.assert_called_with(self.bsn)

        product = response[0]
        self.assertEqual(product, self.product_transformed)

    @patch("app.focus_service_aanvragen.get_client")
    def test_get_aanvraag_no_show(self, get_client_mock):
        mock_client = MockClient(
            name="getAanvragen",
            response=create_soap_response_get_aanvragen("BlablaDingen", None),
        )
        get_client_mock.return_value = mock_client
        response = get_aanvragen(bsn=self.bsn)

        self.assertTrue(len(response) == 0)
        self.assertEqual(response, [])
        mock_client.service.getAanvragen.assert_called_with(self.bsn)


class TestFocusStadspasAanvraag2(TestCase):

    bsn = 99321321321
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
            "beslissing": None,
            "bezwaar": None,
            "herstelTermijn": None,
            "inBehandeling": None,
        },
        "typeBesluit": None,
    }

    product_transformed = {
        "id": "4b46c9865ac4f007b2b0fdd03fd1fbba",
        "title": "Stadspas",
        "status": "aanvraag",
        "decision": None,
        "datePublished": "2019-05-08T15:05:52",
        "dateStart": "2019-05-08T15:05:52",
        "dateEnd": None,
        "steps": [
            {
                "id": "aanvraag",
                "title": "Aanvraag",
                "documents": [
                    {
                        "id": "4400000013",
                        "title": "Aanvraag Stadspas (balie)",
                        "url": "/wpi/aanvraag/document?id=4400000013&isBulk=True&isDms=False",
                        "datePublished": "2019-05-08T15:05:52",
                    }
                ],
                "datePublished": "2019-05-08T15:05:52",
            },
        ],
    }

    @patch("app.focus_service_aanvragen.get_client")
    def test_get_aanvraag_start(self, get_client_mock):
        mock_client = MockClient(
            name="getAanvragen",
            response=create_soap_response_get_aanvragen(
                "Minimafonds", self.product_source
            ),
        )
        get_client_mock.return_value = mock_client
        response = get_aanvragen(bsn=self.bsn)

        self.assertTrue(len(response) == 1)
        mock_client.service.getAanvragen.assert_called_with(self.bsn)

        product = response[0]
        self.assertEqual(product, self.product_transformed)


class TestFocusService(TestCase):
    @patch("app.focus_service_aanvragen.FOCUS_WSDL", "http://some/path/to/wsdl")
    @patch("app.focus_service_aanvragen.FOCUS_USERNAME", "username")
    @patch("app.focus_service_aanvragen.FOCUS_PASSWORD", "password")
    @patch("app.focus_service_aanvragen.Client")
    @patch("app.focus_service_aanvragen.Settings")
    @patch("app.focus_service_aanvragen.Session")
    @patch("app.focus_service_aanvragen.Transport")
    @patch("app.focus_service_aanvragen.HTTPBasicAuth")
    def test_get_client(
        self, basic_auth_mock, transport_mock, session_mock, settings_mock, client_mock
    ):
        result = get_client()

        basic_auth_mock.assert_called_with("username", "password")
        self.assertTrue(hasattr(session_mock, "auth"))
        transport_mock.assert_called_with(
            timeout=30,
            operation_timeout=30,
            session=session_mock(),
        )
        client_mock.assert_called_with(
            wsdl="http://some/path/to/wsdl",
            transport=transport_mock(),
            settings=settings_mock(),
        )
        self.assertEqual(result, client_mock())

        client_mock.reset_mock()

        # Client is cached
        result = get_client()

        client_mock.assert_not_called()

        self.assertEqual(result, client_mock())

    def test_get_decision(self):
        result = get_decision("HeY    Ho")
        result_expected = "heyho"
        self.assertEqual(result, result_expected)

    @patch(
        "app.focus_service_aanvragen.FOCUS_TITLE_TRANSLATIONS",
        {"test": "123", "foo": "bar"},
    )
    def test_get_translation(self):
        result = get_translation("test")
        result_expected = "123"
        self.assertEqual(result, result_expected)

        result = get_translation("foo")
        result_expected = "bar"
        self.assertEqual(result, result_expected)

        result = get_translation("some")
        result_expected = "some"
        self.assertEqual(result, result_expected)

    @patch(
        "app.focus_service_aanvragen.FOCUS_STEP_ID_TRANSLATIONS",
        {"step1": "Stap 1"},
    )
    def test_get_step_title(self):
        result = get_step_title("step1")
        result_expected = "Stap 1"
        self.assertEqual(result, result_expected)

        result = get_translation("some")
        result_expected = "some"
        self.assertEqual(result, result_expected)

    def test_calculate_municipality_feedback_date_max(self):
        result = calculate_municipality_feedback_date_max(
            base_date=datetime.datetime(2022, 2, 1),
            aantal_dagen_dienstverleningstermijn=21,
            aantal_dagen_inspanningsperiode=28,
            aantal_dagen_hersteltermijn=0,
        )
        result_expected = datetime.datetime(2022, 3, 22, 0, 0)
        self.assertEqual(result, result_expected)

        result = calculate_municipality_feedback_date_max(
            base_date=datetime.datetime(2022, 2, 1),
            aantal_dagen_dienstverleningstermijn=21,
            aantal_dagen_inspanningsperiode=28,
            aantal_dagen_hersteltermijn=10,
        )
        result_expected = datetime.datetime(2022, 4, 1, 0, 0)
        self.assertEqual(result, result_expected)

    def test_calculate_user_feedback_date_max(self):
        result = calculate_user_feedback_date_max(
            datetime.datetime(2022, 2, 1), aantal_dagen_hersteltermijn=10
        )
        result_expected = datetime.datetime(2022, 2, 11, 0, 0)
        self.assertEqual(result, result_expected)

    @patch(
        "app.focus_service_aanvragen.FOCUS_DOCUMENT_PATH", "/document/download/endpoint"
    )
    def test_get_document_url(self):
        result = get_document_url(
            {
                "id": "test1",
                "isBulk": True,
                "isDms": False,
            },
            "http://path/to/api",
        )
        result_expected = "http://path/to/api/document/download/endpoint?id=test1&isBulk=True&isDms=False"
        self.assertEqual(result, result_expected)

    # get_document_url,get_translation
    @patch("app.focus_service_aanvragen.get_document_url")
    @patch("app.focus_service_aanvragen.get_translation")
    def test_transform_step_documents(
        self, get_translation_mock, get_document_url_mock
    ):
        get_translation_mock.return_value = "bar"
        get_document_url_mock.return_value = "foo"

        document = {
            "id": "4400000007",
            "isBulk": True,
            "isDms": False,
            "omschrijving": "Formulier Inlichtingen Klant",
        }
        step = {
            "datum": datetime.datetime(2019, 5, 8, 15, 5, 52),
            "document": [
                document,
            ],
        }

        result = transform_step_documents(step)

        get_translation_mock.assert_called_with("Formulier Inlichtingen Klant")
        get_document_url_mock.assert_called_with(document)

        result_expected = [
            {
                "id": "4400000007",
                "title": "bar",
                "url": "foo",
                "datePublished": "2019-05-08T15:05:52",
            }
        ]

        self.assertEqual(result, result_expected)
