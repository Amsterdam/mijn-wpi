import datetime
import os
from unittest.mock import patch

from app.test_app import WpiApiTestApp
from app.test_focus_service_aanvragen import TestFocusBijstandAanvraag
from app.test_focus_service_e_aanvraag import example_result


@patch.dict(
    os.environ,
    {
        "MA_BUILD_ID": "999",
        "MA_GIT_SHA": "abcdefghijk",
        "MA_OTAP_ENV": "unittesting",
    },
)
class WPITestServer(WpiApiTestApp):
    def test_status(self):
        response = self.client.get("/status/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.decode(),
            '{"content":{"buildId":"999","gitSha":"abcdefghijk","otapEnv":"unittesting"},"status":"OK"}\n',
        )

    @patch("app.server.get_aanvragen")
    def test_aanvragen(self, get_aanvragen_mock):
        get_aanvragen_mock.return_value = [
            TestFocusBijstandAanvraag.product_transformed
        ]

        response = self.get_secure("/wpi/uitkering/aanvragen")
        response_json = response.get_json()

        get_aanvragen_mock.assert_called_with(self.TEST_BSN)

        self.assertEqual(
            response_json["content"], [TestFocusBijstandAanvraag.product_transformed]
        )

    def test_aanvragen_fail(self):
        response = self.client.get("/wpi/uitkering/aanvragen")
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
