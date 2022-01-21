import json
import os
from unittest import TestCase

from mock import patch
from tests.focus_test_app import FocusApiTestApp

# Prepare environment
from tests.mocks import MockClient

os.environ["FOCUS_USERNAME"] = "FOCUS_USERNAME"
os.environ["FOCUS_PASSWORD"] = "FOCUS_PASSWORD"
os.environ["FOCUS_WSDL"] = "focus/focus.wsdl"
os.environ["TMA_CERTIFICATE"] = __file__


from app.config import config, credentials
from app.focusconnect import FocusConnection
from app.focusinterpreter import _to_bool, _to_int, _to_list, convert_aanvragen

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


# side step decoding the BSN from SAML token
@patch("app.server.get_bsn_from_request", lambda: 123456789)
@patch("app.focusconnect.Client", new=MockClient)
class TestApi(FocusApiTestApp):
    @patch(
        "app.focusconnect.FocusConnection.aanvragen",
        new=lambda s, bsn, url_root: {"aap": "noot"},
    )
    def test_verhuizingen_with_connection(self):
        """
        Expect a result with meldingen
        """
        response = self.client.get("/focus/aanvragen")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result["aap"], "noot")


class TestConnection(TestCase):
    @patch.object(FocusConnection, "_initialize_client")
    def test_service_set_up(self, mocked_set_client):
        """
        Test if the service is established on object creation time
        :return:
        """
        FocusConnection(config, credentials)
        self.assertTrue(mocked_set_client.called)


class TestHealth(FocusApiTestApp):
    def test_health(self):
        """
        Simple respond OK when the API is up
        :return:
        """
        response = self.client.get("/status/health")
        self.assertEqual(response.status_code, 200)


class TestData(FocusApiTestApp):
    @patch("app.focusconnect.FocusConnection._initialize_client", new=lambda s: "Dummy")
    def test_data_with_connection(self):
        """
        The connection should be marked as available when a client is set
        """
        response = self.client.get("/status/data")
        self.assertEqual(response.status_code, 200)

    @patch("app.focusconnect.FocusConnection._initialize_client", new=lambda s: None)
    def test_data_without_connection(self):
        """
        The connection is not available in test mode, expect 500
        """
        response = self.client.get("/status/data")
        self.assertEqual(response.status_code, 500)


class TestInterpreter(FocusApiTestApp):
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

        tests = [
            {"input": {"bsn": 123}, "expected": [], "url_root": ""},
            {"input": {"bsn": 123, "soortProduct": {}}, "expected": [], "url_root": ""},
            {
                "input": {
                    "bsn": 123,
                    "soortProduct": {
                        "naam": "soortProduct",
                        "product": {
                            "dienstverleningstermijn": "30",
                            "inspanningsperiode": "50",
                        },
                    },
                },
                "expected": [
                    {
                        "_id": "0-0",
                        "_meest_recent": None,
                        "soortProduct": "soortProduct",
                        "dienstverleningstermijn": 30,
                        "inspanningsperiode": 50,
                    }
                ],
                "url_root": "",
            },
            {
                "input": {
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
                                        "isDms": "true",
                                    }
                                }
                            },
                        },
                    },
                },
                "expected": [
                    {
                        "_id": "0-0",
                        "_meest_recent": "aanvraag",
                        "soortProduct": "soortProduct",
                        "dienstverleningstermijn": 30,
                        "inspanningsperiode": 50,
                        "processtappen": {
                            "aanvraag": {
                                "_id": 0,
                                "document": [
                                    {
                                        "$ref": "http://localhost/focus/document?id=1&isBulk=false&isDms=true",
                                        "id": "1",
                                        "isBulk": False,
                                        "isDms": True,
                                    }
                                ],
                            }
                        },
                    }
                ],
                "url_root": "http://localhost/",
            },
            {
                "input": {
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
                                        "isDms": "true",
                                    },
                                },
                                "beslissing": {
                                    "datum": "123",
                                    "document": {
                                        "id": "1",
                                        "isBulk": "false",
                                        "isDms": "true",
                                    },
                                },
                            },
                        },
                    },
                },
                "expected": [
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
                                "document": [
                                    {
                                        "$ref": "http://localhost/focus/document?id=1&isBulk=false&isDms=true",
                                        "id": "1",
                                        "isBulk": False,
                                        "isDms": True,
                                    }
                                ],
                            },
                            "beslissing": {
                                "_id": 3,
                                "datum": "123",
                                "document": [
                                    {
                                        "$ref": "http://localhost/focus/document?id=1&isBulk=false&isDms=true",
                                        "id": "1",
                                        "isBulk": False,
                                        "isDms": True,
                                    }
                                ],
                            },
                        },
                    }
                ],
                "url_root": "http://localhost/",
            },
            {
                "input": {
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
                                        "isDms": "true",
                                    },
                                },
                                "beslissing": {
                                    "datum": "123",
                                    "document": {
                                        "id": "1",
                                        "isBulk": "false",
                                        "isDms": "true",
                                    },
                                },
                            },
                        },
                    },
                },
                "expected": [
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
                                "document": [
                                    {
                                        "$ref": "http://localhost/focus/document?id=1&isBulk=false&isDms=true",
                                        "id": "1",
                                        "isBulk": False,
                                        "isDms": True,
                                    }
                                ],
                            },
                            "beslissing": {
                                "_id": 3,
                                "datum": "123",
                                "document": [
                                    {
                                        "$ref": "http://localhost/focus/document?id=1&isBulk=false&isDms=true",
                                        "id": "1",
                                        "isBulk": False,
                                        "isDms": True,
                                    }
                                ],
                            },
                        },
                    }
                ],
                "url_root": "http://localhost/",
            },
        ]

        for values in tests:
            converted = convert_aanvragen(values["input"], values["url_root"])
            self.assertEqual(converted, values["expected"])
