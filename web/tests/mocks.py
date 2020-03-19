# Mock the soap client
import os

from focus.config import BASE_PATH


class MockClient:
    def __init__(self, wsdl, transport):
        self.service = MockService()

    def options(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockService:
    def getDocument(self, bsn, id, isBulk, isDms):
        return get_document()

    def getJaaropgaven(self, bsn):
        return MockResponse(reply=jaaropgaven_reponse)

    def getAanvragen(self, bsn):
        return MockResponse(reply=aanvragen_response)

    def getUitkeringspecificaties(self, bsn):
        return MockResponse(reply=uitkeringsspecificaties_response)


class MockResponse:
    def __init__(self, reply):
        self.reply = reply

    @property
    def content(self):
        return self.reply


# this document is from acc
TEST_PDF_PATH = os.path.join(BASE_PATH, 'tests', 'test.pdf')
with open(TEST_PDF_PATH, 'rb') as fh:
    pdf_document = fh.read()

JAAROPGAVEN_RESPONSE_PATH = os.path.join(BASE_PATH, 'tests', 'responses', 'jaaropgaven.xml')
with open(JAAROPGAVEN_RESPONSE_PATH, 'rb') as fp:
    jaaropgaven_reponse = fp.read()

AANVRAGEN_RESPONSE_PATH = os.path.join(BASE_PATH, 'tests', 'responses', 'aanvragen.xml')
with open(AANVRAGEN_RESPONSE_PATH, 'rb') as fp:
    aanvragen_response = fp.read()

INKOMENSSPECIFICATIES_RESPONSE_PATH = os.path.join(BASE_PATH, 'tests', 'responses', 'uitkeringsspecificaties.xml')
with open(INKOMENSSPECIFICATIES_RESPONSE_PATH, 'rb') as fp:
    uitkeringsspecificaties_response = fp.read()


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
        'fileName': r'TestIKB\TestBulk15.pdf'
    }
    return document
