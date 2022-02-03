from unittest.mock import patch

from tma_saml.for_tests.cert_and_key import server_crt

from app.test_app import WpiApiTestApp
from app.utils import encrypt


@patch("app.utils.ENABLE_OPENAPI_VALIDATION", False)
@patch("app.utils.get_tma_certificate", lambda: server_crt)
class WPITestServer(WpiApiTestApp):
    def test_status_health(self):
        response = self.client.get("/status/health")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["content"], "OK")

    @patch("app.server.get_aanvragen")
    def test_aanvragen(self, get_aanvragen_mock):
        get_aanvragen_mock.return_value = ["Aanvragen"]

        response = self.get_secure("/wpi/aanvragen")
        response_json = response.get_json()

        get_aanvragen_mock.assert_called_with(self.TEST_BSN)

        self.assertEqual(response_json["content"], ["Aanvragen"])

    @patch("app.server.get_document")
    def test_document(self, get_document_mock):
        get_document_mock.return_value = {
            "file_name": "some_document_file_name.pdf",
            "document_content": "document_content_bytes",
            "mime_type": "mime/testing",
        }

        response = self.get_secure(
            "/wpi/document?id=test-id-xcfg&isDms=False&isBulk=True",
        )

        get_document_mock.assert_called_with(self.TEST_BSN, "test-id-xcfg", True, False)

        self.assertEqual(
            response.headers["Content-Disposition"],
            'attachment; filename="some_document_file_name.pdf"',
        )
        self.assertEqual(response.headers["Content-Type"], "mime/testing")
        self.assertEqual(response.data, b"document_content_bytes")

    @patch("app.server.get_jaaropgaven")
    @patch("app.server.get_uitkeringsspecificaties")
    def test_jaaropgaven(self, get_specificaties_mock, get_jaaropgaven_mock):
        get_specificaties_mock.return_value = ["Uitkeringsspecificaties"]
        get_jaaropgaven_mock.return_value = ["Jaaropgaven"]

        response = self.get_secure(
            "/wpi/bijstanduitkering/specificaties-en-jaaropgaven"
        )

        response_json = response.get_json()

        get_jaaropgaven_mock.assert_called_with(self.TEST_BSN)

        self.assertEqual(
            response_json["content"],
            {
                "jaaropgaven": ["Jaaropgaven"],
                "uitkeringsspecificaties": ["Uitkeringsspecificaties"],
            },
        )

    @patch("app.server.get_stadspas_admin_number")
    @patch("app.server.get_stadspassen")
    def test_stadspassen(self, get_stadspassen_mock, get_stadspas_admin_number_mock):
        get_stadspassen_mock.return_value = ["Stadspassen"]
        get_stadspas_admin_number_mock.return_value = {
            "admin_number": "abcdefg123",
            "type": "hoofdpashouder",
        }

        response = self.get_secure("/wpi/stadspas")
        response_json = response.get_json()

        response_expected = {
            "stadspassen": ["Stadspassen"],
            "ownerType": "hoofdpashouder",
            "adminNumber": "abcdefg123",
        }

        self.assertEqual(response_json["content"], response_expected)

    @patch(
        "app.utils.GPASS_FERNET_ENCRYPTION_KEY",
        "z4QX3k3bj61ST2HRRV7dnn7Se8VFCaHscK39JfODz8s=",
    )
    @patch("app.server.get_transactions")
    def test_stadspastransactions(self, get_stadspastransactions_mock):
        get_stadspastransactions_mock.return_value = ["Transacties"]

        transactions_key = encrypt("123abc", "abcdefg123", "0009998887777")

        response = self.get_secure(f"/wpi/stadspas/transacties/{transactions_key}")
        response_json = response.get_json()

        get_stadspastransactions_mock.assert_called_with(
            "abcdefg123", "0009998887777", "123abc"
        )

        self.assertEqual(response_json["content"], ["Transacties"])
