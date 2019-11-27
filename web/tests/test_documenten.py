import os.path
from unittest import TestCase

# Prepare environment
from flask_testing import TestCase as FlaskTestCase
from mock import patch

os.environ['FOCUS_USERNAME'] = 'FOCUS_USERNAME'
os.environ['FOCUS_PASSWORD'] = 'FOCUS_PASSWORD'
os.environ['FOCUS_WSDL'] = 'focus/focus.wsdl'
os.environ['TMA_CERTIFICATE'] = __file__

from focus.config import BASE_PATH, config, credentials  # noqa: E402  Module level import not at top of file
from focus.focusconnect import FocusConnection  # noqa: E402
from focus.server import application  # noqa: E402


# this document is from acc
TEST_PDF_PATH = os.path.join(BASE_PATH, 'tests', 'test.pdf')
with open(TEST_PDF_PATH, 'rb') as fh:
    pdf_document = fh.read()


# Mock the soap client
class MockClient:
    def __init__(self, wsdl, transport):
        self.service = MockService()


class MockService:
    def getDocument(self, bsn, id, isBulk, isDms):
        return get_document()


def get_document():
    # obtained from acc
    document = {
        'contentID': None,
        'contentLanguage': [],
        'contentMD5': None,
        'dataHandler': pdf_document,
        'description': None,
        'disposition': 'attachment',
        'document': None,
        'fileName': 'TestIKB\\TestBulk15.pdf'
    }
    return document


@patch('focus.focusconnect.Client', new=MockClient)
class DocumentTest(TestCase):
    def test_focus_connection_document(self):
        focus_connection = FocusConnection(config, credentials)

        doc = focus_connection.document(id=1, bsn="12345", isBulk=True, isDms=False)
        self.assertEqual(doc['fileName'], 'TestIKB\\TestBulk15.pdf')
        self.assertEqual(doc['mime_type'], 'application/pdf')
        self.assertEqual(doc['contents'], pdf_document)


@patch('focus.focusconnect.Client', new=MockClient)
# side step decoding the BSN from SAML token
@patch('focus.focusserver.get_bsn_from_request', new=lambda s: 123456789)
class DocumentApiTest(FlaskTestCase):
    def create_app(self):
        return application

    def test_document_api(self):
        response = self.client.get('/focus/document?id=1&isBulk=true&isDms=true')
        self.assertEqual(response.data, pdf_document)
        self.assertEqual(response.headers['Content-Disposition'], r'attachment; filename="TestIKB\\TestBulk15.pdf"')
