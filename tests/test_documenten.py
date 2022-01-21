import os.path
from unittest import TestCase

# Prepare environment
from mock import patch
from tests.focus_test_app import FocusApiTestApp

from tests.mocks import MockClient, pdf_document

os.environ["FOCUS_USERNAME"] = "FOCUS_USERNAME"
os.environ["FOCUS_PASSWORD"] = "FOCUS_PASSWORD"
os.environ["FOCUS_WSDL"] = "focus/focus.wsdl"
os.environ["TMA_CERTIFICATE"] = __file__

from app.config import (
    config,
    credentials,
)  # noqa: E402  Module level import not at top of file
from app.focusconnect import FocusConnection  # noqa: E402


@patch("app.focusconnect.Client", new=MockClient)
class DocumentTest(TestCase):
    def test_focus_connection_document(self):
        focus_connection = FocusConnection(config, credentials)

        doc = focus_connection.document(id=1, bsn="12345", isBulk=True, isDms=False)
        self.assertEqual(doc["fileName"], "TestIKB\\TestBulk15.pdf")
        self.assertEqual(doc["mime_type"], "application/pdf")
        self.assertEqual(doc["contents"], pdf_document)


# side step decoding the BSN from SAML token
@patch("app.focusserver.get_bsn_from_request", new=lambda s: "123456789")
@patch("app.focusconnect.Client", new=MockClient)
class DocumentApiTest(FocusApiTestApp):
    def test_document_api(self):
        response = self.client.get("/focus/document?id=1&isBulk=true&isDms=true")
        self.assertEqual(response.data, pdf_document)
        self.assertEqual(
            response.headers["Content-Disposition"],
            r'attachment; filename="TestIKB\TestBulk15.pdf"',
        )
