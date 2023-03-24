import datetime
from unittest.mock import patch

from app.test_app import WpiApiTestApp
from app.test_focus_service_aanvragen import TestFocusBijstandAanvraag
from app.test_focus_service_e_aanvraag import example_result
from app.test_gpass_service import GpassServiceGetStadspas
from app.utils import encrypt


@patch("app.utils.ENABLE_OPENAPI_VALIDATION", True)
class WPITestServer(WpiApiTestApp):
    def test_status_health(self):
        response = self.client.get("/status/health")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["content"], "OK")

    @patch("app.server.get_aanvragen")
    def test_aanvragen(self, get_aanvragen_mock):
        get_aanvragen_mock.return_value = [
            TestFocusBijstandAanvraag.product_transformed
        ]

        response = self.get_secure("/wpi/uitkering-en-stadspas/aanvragen")
        response_json = response.get_json()

        get_aanvragen_mock.assert_called_with(self.TEST_BSN)

        self.assertEqual(
            response_json["content"], [TestFocusBijstandAanvraag.product_transformed]
        )

    def test_aanvragen_fail(self):
        response = self.client.get("/wpi/uitkering-en-stadspas/aanvragen")
        response_json = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json["status"], "ERROR")

    @patch("app.server.get_e_aanvragen")
    def test_e_aanvragen(self, get_e_aanvragen_mock):
        get_e_aanvragen_mock.return_value = example_result

        response = self.get_secure("/wpi/e-aanvragen")
        response_json = response.get_json()

        get_e_aanvragen_mock.assert_called_with(self.TEST_BSN)

        self.assertEqual(response_json["content"], example_result)

    @patch("app.server.get_document")
    def test_document(self, get_document_mock):
        get_document_mock.return_value = {
            "file_name": "some_document_file_name.pdf",
            "document_content": "document_content_bytes",
            "mime_type": "application/pdf",
        }

        response = self.get_secure(
            "/wpi/document?id=test-id-xcfg&isDms=False&isBulk=True",
        )

        get_document_mock.assert_called_with(self.TEST_BSN, "test-id-xcfg", True, False)

        self.assertEqual(
            response.headers["Content-Disposition"],
            'attachment; filename="some_document_file_name.pdf"',
        )
        self.assertEqual(response.headers["Content-Type"], "application/pdf")
        self.assertEqual(response.data, b"document_content_bytes")

    @patch("app.server.get_jaaropgaven")
    @patch("app.server.get_uitkeringsspecificaties")
    def test_jaaropgaven(self, get_specificaties_mock, get_jaaropgaven_mock):
        def create_specificatie(title, dcteId, date_published):
            return {
                "datePublished": date_published.isoformat(),
                "id": dcteId,
                "title": f"{title} {date_published.year}",
                "variant": "",
                "url": f"http://doc/{dcteId}",
            }

        specification = create_specificatie(
            "test1", "1a", datetime.datetime(2020, 1, 5, 0, 0)
        )
        get_specificaties_mock.return_value = [specification]
        jaaropgave = create_specificatie(
            "test2", "2b", datetime.datetime(2021, 3, 15, 0, 0)
        )
        get_jaaropgaven_mock.return_value = [jaaropgave]

        response = self.get_secure("/wpi/uitkering/specificaties-en-jaaropgaven")
        response_json = response.get_json()

        get_jaaropgaven_mock.assert_called_with(self.TEST_BSN)

        self.assertEqual(
            response_json["content"],
            {
                "jaaropgaven": [jaaropgave],
                "uitkeringsspecificaties": [specification],
            },
        )

    @patch("app.server.get_clientnummer")
    @patch("app.server.get_stadspas_admin_number")
    @patch("app.server.get_stadspassen")
    def test_stadspassen(self, get_stadspassen_mock, get_stadspas_admin_number_mock, get_clientnummer_mock):
        get_stadspassen_mock.return_value = [GpassServiceGetStadspas.gpass_formatted]
        get_stadspas_admin_number_mock.return_value = {
            "admin_number": "abcdefg123",
            "type": "hoofdpashouder",
        }
        get_clientnummer_mock.return_value = None

        response = self.get_secure("/wpi/stadspas")
        response_json = response.get_json()

        response_expected = {
            "stadspassen": [GpassServiceGetStadspas.gpass_formatted],
            "ownerType": "hoofdpashouder",
            "adminNumber": "abcdefg123",
        }

        self.assertEqual(response_json["content"], response_expected)

    @patch("app.server.get_clientnummer")
    @patch("app.server.get_stadspas_admin_number")
    @patch("app.server.get_stadspassen")
    def test_stadspassen_with_zorgned_result(self, get_stadspassen_mock, get_stadspas_admin_number_mock, get_clientnummer_mock):
        get_stadspassen_mock.return_value = [GpassServiceGetStadspas.gpass_formatted]
        get_stadspas_admin_number_mock.return_value = {
            "admin_number": "abcdefg123",
            "type": "hoofdpashouder",
        }
        get_clientnummer_mock.return_value = 123

        response = self.get_secure("/wpi/stadspas")
        response_json = response.get_json()

        response_expected = {
            "stadspassen": [GpassServiceGetStadspas.gpass_formatted],
            "ownerType": "hoofdpashouder",
            "adminNumber": "03630000000123",
        }

        self.assertEqual(response_json["content"], response_expected)

    @patch(
        "app.utils.GPASS_FERNET_ENCRYPTION_KEY",
        "z4QX3k3bj61ST2HRRV7dnn7Se8VFCaHscK39JfODz8s=",
    )
    @patch("app.server.get_transactions")
    def test_stadspastransactions(self, get_stadspastransactions_mock):
        transaction_dummy = {
            "id": "test",
            "title": "Budget title",
            "amount": 50,
            "datePublished": "2022-02-25T13:55:02.000",
        }
        get_stadspastransactions_mock.return_value = [
            {
                "id": "test",
                "title": "Budget title",
                "amount": 50,
                "datePublished": "2022-02-25T13:55:02.000",
            }
        ]

        transactions_key = encrypt("123abc", "abcdefg123", "0009998887777")

        response = self.get_secure(f"/wpi/stadspas/transacties/{transactions_key}")
        response_json = response.get_json()

        get_stadspastransactions_mock.assert_called_with(
            "abcdefg123", "0009998887777", "123abc"
        )

        self.assertEqual(response_json["content"], [transaction_dummy])
