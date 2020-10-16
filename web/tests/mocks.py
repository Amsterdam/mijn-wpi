# Mock the soap client
import json
import os

from focus.config import BASE_PATH

RESPONSES_PATH = os.path.join(BASE_PATH, 'tests', 'responses')


class MockClient:
    def __init__(self, wsdl, transport):
        self.service = MockService()

    def settings(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockClientEmpties:
    def __init__(self, wsdl, transport):
        self.service = MockServiceEmpties()

    def settings(self, *args, **kwargs):
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

    def getEAanvraagTOZO(self, bsn):
        return MockResponse(reply=tozo_documenten_response)

    def getStadspas(self, bsn):
        return MockResponse(reply=stadspas_response)


class MockServiceEmpties:
    def getDocument(self, bsn, id, isBulk, isDms):
        return get_document()

    # def getJaaropgaven(self, bsn):
    #     return MockResponse(reply=jaaropgaven_reponse)
    #
    # def getAanvragen(self, bsn):
    #     return MockResponse(reply=aanvragen_response)
    #
    # def getUitkeringspecificaties(self, bsn):
    #     return MockResponse(reply=uitkeringsspecificaties_response)

    def getEAanvraagTOZO(self, bsn):
        return MockResponse(reply=tozo_documenten_empty_response)


def get_response_mock(*args, **kwargs):
    """ Attempt to get data from mock_get_urls. """
    try:
        res_data = mocked_get_urls[args[0]]
    except KeyError:
        return MockResponse('', 404)
        # raise Exception("Url not defined %s", args[0])
    return MockResponse(res_data)


class MockResponse:
    def __init__(self, reply, status_code=200):
        self.reply = reply
        self.status_code = status_code

    @property
    def content(self):
        return self.reply

    @property
    def data(self):
        return self.reply

    def json(self):
        return self.data


# this document is from acc
TEST_PDF_PATH = os.path.join(BASE_PATH, 'tests', 'test.pdf')
with open(TEST_PDF_PATH, 'rb') as fh:
    pdf_document = fh.read()

JAAROPGAVEN_RESPONSE_PATH = os.path.join(RESPONSES_PATH, 'jaaropgaven.xml')
with open(JAAROPGAVEN_RESPONSE_PATH, 'rb') as fp:
    jaaropgaven_reponse = fp.read()

AANVRAGEN_RESPONSE_PATH = os.path.join(RESPONSES_PATH, 'aanvragen.xml')
with open(AANVRAGEN_RESPONSE_PATH, 'rb') as fp:
    aanvragen_response = fp.read()

INKOMENSSPECIFICATIES_RESPONSE_PATH = os.path.join(RESPONSES_PATH, 'uitkeringsspecificaties.xml')
with open(INKOMENSSPECIFICATIES_RESPONSE_PATH, 'rb') as fp:
    uitkeringsspecificaties_response = fp.read()

TOZO_DOCUMENTEN_RESPONSE_PATH = os.path.join(RESPONSES_PATH, 'tozo_documenten.xml')
with open(TOZO_DOCUMENTEN_RESPONSE_PATH, 'rb') as fp:
    tozo_documenten_response = fp.read()

TOZO_DOCUMENTEN_EMPTY_RESPONSE_PATH = os.path.join(RESPONSES_PATH, 'tozo_documenten_empty.xml')
with open(TOZO_DOCUMENTEN_EMPTY_RESPONSE_PATH, 'rb') as fp:
    tozo_documenten_empty_response = fp.read()

STADSPAS_RESPONSE_PATH = os.path.join(RESPONSES_PATH, 'stadspas.xml')
with open(STADSPAS_RESPONSE_PATH, 'rb') as fp:
    stadspas_response = fp.read()


def _load_fixture(json_file_name):
    with open(os.path.join(RESPONSES_PATH, json_file_name)) as fh:
        return json.load(fh)


def _load_fixture_as_bytes(file_name):
    with open(os.path.join(RESPONSES_PATH, file_name)) as fh:
        return fh.read()


mocked_get_urls_tuple = (
    (
        "http://localhost/decosweb/aspx/api/v1/items/32charsstringxxxxxxxxxxxxxxxxxxx/folders?select=title,mark,text45,subject1,text9,text11,text12,text13,text6,date6,text7,text10,date7,text8,document_date,date5,processed,dfunction&top=10",
        _load_fixture_as_bytes('stadspas.xml')
    ),
    (
        "http://localhost/rest/sales/v1/pashouder?addsubs=true",
        _load_fixture('gpass/pashouder.json')
    ),
    (
        "http://localhost/rest/sales/v1/pas/6666666666666?include_balance=true",
        _load_fixture('gpass/pas1.json')
    ),
    (
        "http://localhost/rest/transacties/v1/budget?pasnummer=6666666666666",
        _load_fixture("gpass/transactions.json")
    )
)
mocked_get_urls = dict(mocked_get_urls_tuple)


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
