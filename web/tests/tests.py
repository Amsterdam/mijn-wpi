import os
import json
from base64 import b64encode, b64decode
from xml.etree import ElementTree

from flask_testing.utils import TestCase
from lxml import etree
from mock import patch
from signxml import XMLSigner
import hiro as hiro


'''Prepare environment'''
os.environ['FOCUS_USERNAME'] = 'FOCUS_USERNAME'
os.environ['FOCUS_PASSWORD'] = 'FOCUS_PASSWORD'
os.environ['FOCUS_WSDL'] = 'focus/focus.wsdl'

test_dir = os.path.dirname(os.path.realpath(__file__))


from focus.config import config, credentials
from focus.focusconnect import FocusConnection
from focus.focusinterpreter import _to_list, _to_type, _to_int, _to_bool, convert_aanvragen
from focus.saml import verify_saml_token_and_retrieve_saml_attribute, SamlVerificationException
from focus.server import application
import focus.server


unencrypted_saml_token = b"""
<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" ID="234567890" Version="2.0">
    <saml:AttributeStatement>
        <saml:Attribute Name="uid">
            <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema"
                                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                 xsi:type="xs:string">123456789</saml:AttributeValue>
        </saml:Attribute>
    </saml:AttributeStatement>
</saml:Assertion>
"""


def generate_dummy_saml_token():
    """
    Generate a freshly signed and base64 encoded SAML token which is similar to
    the one TMA gives us, but using test a certificate.

    :return: a base 64 encoded string with a SAML token
    """
    xml_root = ElementTree.fromstring(unencrypted_saml_token)
    signer = XMLSigner()
    with open(os.path.join(test_dir, 'test_tma_cert.crt'), 'rb') as cert_file:
        with open(os.path.join(test_dir, 'test_tma_cert.key'), 'rb') as key_file:
            cert = cert_file.read()
            key = key_file.read()
            signed_root = signer.sign(xml_root, key=key, cert=cert)

            token_string = etree.tostring(signed_root, pretty_print=True)
            return b64encode(token_string)


def get_fake_tma_cert():
    return "fake cert"


@patch('focus.focusconnect.FocusConnection.aanvragen', new=lambda s, bsn, url_root: {'aap': 'noot'})
@patch('focus.focusconnect.FocusConnection._initialize_client', new=lambda s: "Alive")
class TestApiNoToken(TestCase):
    def create_app(self):
        return application

    def test_aanvragen_no_saml_token(self):
        """
        BSN saml token is a required header attribute
        """
        response = self.client.get('/focus/aanvragen')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, b'Parameter error: Missing SAML token')


@patch('focus.server.get_TMA_certificate', new=get_fake_tma_cert)
@patch('focus.focusconnect.FocusConnection._initialize_client', new=lambda s: "Alive")
# side step decoding the BSN from SAML token
@patch('focus.focusserver.get_bsn_from_saml_token', new=lambda s: 123456789)
class TestApi(TestCase):
    def create_app(self):
        return application

    def test_aanvragen(self):
        """
        The connection is not available in test mode, expect 500
        """
        response = self.client.get('/focus/aanvragen')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, b'Focus connectivity failed')

    @patch('focus.focusconnect.FocusConnection.aanvragen', new=lambda s, bsn, url_root: {'aap': 'noot'})
    def test_verhuizingen_with_connection(self):
        """
        Expect a result with meldingen
        """
        response = self.client.get('/focus/aanvragen')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['aap'], 'noot')

    def test_cors_header(self):
        """
        CORS should be enabled
        :return:
        """
        resp = self.client.get(
            '/status/health',
            headers={'Origin': 'http://fee-fi-foo.fum'}
        )
        self.assertTrue('Access-Control-Allow-Origin' in resp.headers)
        self.assertEqual('*', resp.headers['Access-Control-Allow-Origin'])


@patch('focus.server.get_TMA_certificate', new=get_fake_tma_cert)
class TestConnection(TestCase):
    def create_app(self):
        return application

    def setUp(self):
        pass

    @patch.object(FocusConnection, '_initialize_client')
    def test_service_set_up(self, mocked_set_client):
        """
        Test if the service is established on object creation time
        :return:
        """
        FocusConnection(config, credentials)
        self.assertTrue(mocked_set_client.called)


@patch('focus.server.get_TMA_certificate', new=get_fake_tma_cert)
@patch('focus.focusserver.get_bsn_from_saml_token', new=lambda s: 123456789)
class TestRateLimiter(TestCase):
    def create_app(self):
        return application

    def setUp(self):
        application.extensions['limiter'].reset()

    @patch('focus.focusconnect.FocusConnection.aanvragen', new=lambda s, bsn, url_root: {'aap': 'noot'})
    def test_limiter(self):
        url = 'focus/aanvragen'

        # make sure the limiter is enabled
        self.assertTrue(application.extensions['limiter'].enabled)

        # do requests up to the limit, should not limit
        with hiro.Timeline().freeze() as timeline:
            for i in range(5):
                response = self.client.get(url)
                self.assert200(response)

            # do one more, should limit
            response = self.client.get(url)
            self.assertStatus(response, 429)

            # 2 seconds later it should work again
            timeline.forward(2)

            for i in range(5):
                response = self.client.get(url)
                self.assert200(response)

    def test_health_exempt(self):
        """ Make sure that the health check is not limited. """
        self.assertTrue(application.extensions['limiter'].enabled)

        with hiro.Timeline().freeze():
            for i in range(20):  # more than 5 / second
                response = self.client.get('/status/data')
                self.assert200(response)

        with hiro.Timeline().freeze():
            for i in range(20):  # more than 5 / second
                response = self.client.get('/status/health')
                self.assert200(response)


class TestSamlToken(TestCase):
    def create_app(self):
        return application

    def setUp(self):
        self.saml_token = generate_dummy_saml_token()

    def test_saml_token(self):
        with open(os.path.join(test_dir, 'test_tma_cert.crt'), 'rb') as cert_file:
            cert = cert_file.read()
            bsn = verify_saml_token_and_retrieve_saml_attribute(
                saml_token=self.saml_token,
                attribute='uid',
                saml_cert=cert)
            self.assertEqual(bsn, '123456789')

    def test_saml_token_tampered(self):
        saml_token_tampered = b64encode(b64decode(self.saml_token).replace(b'123456789', b'987654321'))
        self.assertNotEqual(self.saml_token, saml_token_tampered)

        with self.assertRaises(SamlVerificationException):
            with open(os.path.join(test_dir, 'test_tma_cert.crt'), 'rb') as cert_file:
                cert = cert_file.read()
                bsn = verify_saml_token_and_retrieve_saml_attribute(
                    saml_token=saml_token_tampered,
                    attribute='uid',
                    saml_cert=cert)


@patch('focus.server.get_TMA_certificate', new=get_fake_tma_cert)
@patch('focus.focusconnect.FocusConnection._initialize_client', new=lambda s: "Alive")
class TestHealth(TestCase):
    def create_app(self):
        return application

    def setUp(self):
        pass

    def test_health(self):
        """
        Simple respond OK when the API is up
        :return:
        """
        response = self.client.get('/status/health')
        self.assertEqual(response.status_code, 200)


@patch('focus.server.get_TMA_certificate', new=get_fake_tma_cert)
class TestData(TestCase):
    def create_app(self):
        focus.server.focus_server = None
        application.extensions['limiter'].enabled = False
        return application

    def setUp(self):
        pass

    def tearDown(self):
        application.extensions['limiter'].enabled = True

    @patch('focus.focusconnect.FocusConnection._initialize_client', new=lambda s: "Dummy")
    def test_data_with_connection(self):
        """
        The connection should be marked as available when a client is set
        """
        response = self.client.get('/status/data')
        self.assertEqual(response.status_code, 200)

    @patch('focus.focusconnect.FocusConnection._initialize_client', new=lambda s: None)
    def test_data_without_connection(self):
        """
        The connection is not available in test mode, expect 500
        """
        response = self.client.get('/status/data')
        self.assertEqual(response.status_code, 500)


class TestInterpreter(TestCase):
    def create_app(self):
        return application

    def setUp(self):
        pass

    def test_to_array(self):
        self.assertEqual(_to_list({}, "x"), {"x": []})
        self.assertEqual(_to_list({"x": []}, "x"), {"x": []})
        self.assertEqual(_to_list({"x": [1, 2]}, "x"), {"x": [1, 2]})
        self.assertEqual(_to_list({"x": {}}, "x"), {"x": [{}]})

    def test__to_type(self):
        self.assertEqual(_to_int({"x": "26"}, "x"), {"x": 26})
        self.assertEqual(_to_int({}, "x"), {})
        with self.assertRaises(ValueError):
            _to_int({"x": "aap"}, "x")
        self.assertEqual(_to_bool({"x": "false"}, "x"), {"x": False})
        self.assertEqual(_to_bool({"x": "true"}, "x"), {"x": True})
        self.assertEqual(_to_bool({"x": ""}, "x"), {"x": False})
        self.assertEqual(_to_bool({"x": "True"}, "x"), {"x": True})
        self.assertEqual(_to_bool({}, "x"), {})

    def test_convert_aanvragen(self):
        self.assertEqual(convert_aanvragen({"bsn": 123}, ""), [])
        self.assertEqual(convert_aanvragen({"bsn": 123, "soortProduct": {}}, ""), [])
        self.assertEqual(convert_aanvragen({
            "bsn": 123,
            "soortProduct": {
                "naam": "soortProduct",
                "product": {
                    "dienstverleningstermijn": "30",
                    "inspanningsperiode": "50"
                }
            }}, ""), [
                        {
                            "_id": "0-0",
                            "_meest_recent": None,
                            "soortProduct": "soortProduct",
                            "dienstverleningstermijn": 30,
                            "inspanningsperiode": 50
                        }
                    ])
        self.assertEqual(convert_aanvragen({
            "bsn": 123,
            "soortProduct": {
                "naam": "soortProduct",
                "product": {
                    "dienstverleningstermijn": "30",
                    "inspanningsperiode": "50",
                    "processtappen": {
                        "aanvraag": {
                            "document": {
                                "id": "1",
                                "isBulk": "false",
                                "isDms": "true"
                            }
                        }
                    }
                }
            }}, "http://xyz.com/"), [
                        {
                            "_id": "0-0",
                            "_meest_recent": "aanvraag",
                            "soortProduct": "soortProduct",
                            "dienstverleningstermijn": 30,
                            "inspanningsperiode": 50,
                            "processtappen": {
                                "aanvraag": {
                                    "_id": 0,
                                    "document": [{
                                        "$ref": "http://xyz.com/focus/document?id=1&isBulk=false&isDms=true",
                                        "id": 1,
                                        "isBulk": False,
                                        "isDms": True
                                    }]
                                }
                            }
                        }
                    ])
        self.assertEqual(convert_aanvragen({
            "bsn": 123,
            "soortProduct": {
                "naam": "soortProduct",
                "product": {
                    "dienstverleningstermijn": "30",
                    "inspanningsperiode": "50",
                    "processtappen": {
                        "aanvraag": {
                            "datum": "123",
                            "document": {
                                "id": "1",
                                "isBulk": "false",
                                "isDms": "true"
                            }
                        },
                        "beslissing": {
                            "datum": "123",
                            "document": {
                                "id": "1",
                                "isBulk": "false",
                                "isDms": "true"
                            }
                        }
                    }
                }
            }}, "http://xyz.com/"), [
                    {
                        "_id": "0-0",
                        "_meest_recent": "beslissing",
                        "soortProduct": "soortProduct",
                        "dienstverleningstermijn": 30,
                        "inspanningsperiode": 50,
                        "processtappen": {
                            "aanvraag": {
                                "_id": 0,
                                "datum": "123",
                                "document": [{
                                    "$ref": "http://xyz.com/focus/document?id=1&isBulk=false&isDms=true",
                                    "id": 1,
                                    "isBulk": False,
                                    "isDms": True
                                }]
                            },
                            "beslissing": {
                                "_id": 3,
                                "datum": "123",
                                "document": [{
                                    "$ref": "http://xyz.com/focus/document?id=1&isBulk=false&isDms=true",
                                    "id": 1,
                                    "isBulk": False,
                                    "isDms": True
                                }]
                            }
                        }
                    }
                ])
        self.assertEqual(convert_aanvragen({
            "bsn": 123,
            "soortProduct": {
                "naam": "soortProduct",
                "product": {
                    "dienstverleningstermijn": "30",
                    "inspanningsperiode": "50",
                    "processtappen": {
                        "aanvraag": {
                            "datum": "234",
                            "document": {
                                "id": "1",
                                "isBulk": "false",
                                "isDms": "true"
                            }
                        },
                        "beslissing": {
                            "datum": "123",
                            "document": {
                                "id": "1",
                                "isBulk": "false",
                                "isDms": "true"
                            }
                        }
                    }
                }
            }}, "http://xyz.com/"), [
                    {
                        "_id": "0-0",
                        "_meest_recent": "aanvraag",
                        "soortProduct": "soortProduct",
                        "dienstverleningstermijn": 30,
                        "inspanningsperiode": 50,
                        "processtappen": {
                            "aanvraag": {
                                "_id": 0,
                                "datum": "234",
                                "document": [{
                                    "$ref": "http://xyz.com/focus/document?id=1&isBulk=false&isDms=true",
                                    "id": 1,
                                    "isBulk": False,
                                    "isDms": True
                                }]
                            },
                            "beslissing": {
                                "_id": 3,
                                "datum": "123",
                                "document": [{
                                    "$ref": "http://xyz.com/focus/document?id=1&isBulk=false&isDms=true",
                                    "id": 1,
                                    "isBulk": False,
                                    "isDms": True
                                }]
                            }
                        }
                    }
                ])
