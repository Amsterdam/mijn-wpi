import os.path
from unittest import TestCase

# Prepare environment
from flask_testing import TestCase as FlaskTestCase
from mock import patch

from web.tests.mocks import MockClient

os.environ['FOCUS_USERNAME'] = 'FOCUS_USERNAME'
os.environ['FOCUS_PASSWORD'] = 'FOCUS_PASSWORD'
os.environ['FOCUS_WSDL'] = 'focus/focus.wsdl'
os.environ['TMA_CERTIFICATE'] = __file__

from focus.config import BASE_PATH, config, credentials  # noqa: E402  Module level import not at top of file
from focus.focusconnect import FocusConnection  # noqa: E402
from focus.server import application  # noqa: E402


@patch('focus.focusconnect.Client', new=MockClient)
class JaaropgavenTest(TestCase):
    def test_connection(self):
        focus_connection = FocusConnection(config, credentials)
        result = focus_connection.jaaropgaven(bsn=1234, url_root='/')
        print(">>>>>>", result)

        assert False


@patch('focus.focusconnect.Client', new=MockClient)
# side step decoding the BSN from SAML token
@patch('focus.focusserver.get_bsn_from_request', new=lambda s: 123456789)
class DocumentApiTest(FlaskTestCase):
    def create_app(self):
        return application

    def test_combined_api(self):
        response = self.client.get('/focus/combined')

        from pprint import pprint
        pprint(response.json)
        assert False
