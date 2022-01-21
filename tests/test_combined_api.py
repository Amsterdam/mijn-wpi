import json
import os.path

# Prepare environment
from mock import patch

from tests.focus_test_app import FocusApiTestApp, get_fake_tma_cert

from .mocks import MockClient, get_response_mock

os.environ["FOCUS_USERNAME"] = "FOCUS_USERNAME"
os.environ["FOCUS_PASSWORD"] = "FOCUS_PASSWORD"
os.environ["FOCUS_WSDL"] = "focus/focus.wsdl"
os.environ["TMA_CERTIFICATE"] = __file__

TESTKEY = "z4QXWk3bjwFST2HRRVidnn7Se8VFCaHscK39JfODzNs="


@patch("app.gpass_service.GPASS_API_LOCATION", "http://localhost")
@patch(
    "app.server.get_bsn_from_request", lambda: 123456789
)  # side step decoding the BSN from SAML token
@patch("app.focusconnect.Client", new=MockClient)
@patch("app.gpass_service.requests.get", get_response_mock)
@patch("app.utils.GPASS_FERNET_ENCRYPTION_KEY", TESTKEY)
class CombinedApiTest(FocusApiTestApp):
    def test_combined_api(self):
        self.maxDiff = None

        response = self.client.get("/focus/combined")

        expected = {
            "content": {
                "jaaropgaven": [
                    {
                        "datePublished": "2011-01-28T00:00:00+01:00",
                        "id": "95330222",
                        "title": "Jaaropgave",
                        "type": "",
                        "url": "focus/document?id=95330222&isBulk=false&isDms=false",
                    },
                    {
                        "datePublished": "2019-01-04T00:00:00+01:00",
                        "id": "20021871",
                        "title": "Jaaropgave",
                        "type": "",
                        "url": "focus/document?id=20021871&isBulk=false&isDms=false",
                    },
                ],
                "uitkeringsspecificaties": [
                    {
                        "datePublished": "2019-04-19T00:00:00+02:00",
                        "id": "24233351",
                        "title": "Uitkeringsspecificatie",
                        "type": "Participatiewet",
                        "url": "focus/document?id=24233351&isBulk=false&isDms=false",
                    },
                    {
                        "datePublished": "2014-01-24T00:00:00+01:00",
                        "id": "30364921",
                        "title": "Uitkeringsspecificatie",
                        "type": "",
                        "url": "focus/document?id=30364921&isBulk=false&isDms=false",
                    },
                ],
                "stadspassaldo": {
                    "type": "hoofpashouder",
                    "stadspassen": [
                        {
                            "budgets": [
                                {
                                    "code": "AMSTEG_10-14",
                                    "description": "Kindtegoed",
                                    "datumAfloop": "2021-08-31T21:59:59.000Z",
                                    "assigned": 150,
                                    "balance": 0,
                                }
                            ],
                            "datumAfloop": "2020-08-31T23:59:59.000Z",
                            "id": 999997,
                            "naam": "J. Doe",
                            "pasnummer": "6011012604737",
                        },
                        {
                            "budgets": [
                                {
                                    "code": "AMSTEG_10-14",
                                    "description": "Kindtegoed",
                                    "datumAfloop": "2021-08-31T21:59:59.000Z",
                                    "assigned": 150,
                                    "balance": 0,
                                }
                            ],
                            "datumAfloop": "2020-08-31T23:59:59.000Z",
                            "id": 999999,
                            "naam": "P Achternaam2",
                            "pasnummer": "6666666666666666666",
                        },
                        {
                            "budgets": [
                                {
                                    "code": "AMSTEG_10-14",
                                    "description": "Kindtegoed",
                                    "datumAfloop": "2021-08-31T21:59:59.000Z",
                                    "assigned": 150,
                                    "balance": 0,
                                }
                            ],
                            "datumAfloop": "2020-08-31T23:59:59.000Z",
                            "id": 999997,
                            "naam": "J Achternaam3",
                            "pasnummer": "6011012604737",
                        },
                    ],
                },
                "tozodocumenten": [
                    {
                        "datePublished": "2020-03-31T18:59:46+02:00",
                        "description": "Tegemoetkoming Ondernemers en Zelfstandigen",
                        "id": "4400000031",
                        "documentCodeId": "770",
                        "type": "E-AANVR-TOZO",
                        "url": "focus/document?id=4400000031&isBulk=true&isDms=false",
                    },
                    {
                        "datePublished": "2020-03-26T15:18:44+01:00",
                        "description": "Verkorte Aanvraag BBZ",
                        "id": "4400000024",
                        "documentCodeId": "756",
                        "type": "E-AANVR-KBBZ",
                        "url": "focus/document?id=4400000024&isBulk=true&isDms=false",
                    },
                    {
                        "datePublished": "2020-03-18T23:09:58+01:00",
                        "description": "Ondernemerscheck zelfstandigen",
                        "id": "4400000020",
                        "documentCodeId": "734",
                        "type": "E-AANVR-DGB",
                        "url": "focus/document?id=4400000020&isBulk=true&isDms=false",
                    },
                    {
                        "datePublished": "2020-03-31T00:21:51+02:00",
                        "description": "Tegemoetkoming Ondernemers en Zelfstandigen",
                        "id": "4400000030",
                        "documentCodeId": "770",
                        "type": "E-AANVR-TOZO",
                        "url": "focus/document?id=4400000030&isBulk=true&isDms=false",
                    },
                    {
                        "datePublished": "2020-03-22T00:26:10+01:00",
                        "description": "Aanvraag BBZ",
                        "id": "4400000022",
                        "documentCodeId": "678",
                        "type": "E-AANVR-BBZ",
                        "url": "focus/document?id=4400000022&isBulk=true&isDms=false",
                    },
                    {
                        "datePublished": "2020-03-31T00:04:34+02:00",
                        "description": "Tegemoetkoming Ondernemers en Zelfstandigen",
                        "id": "4400000029",
                        "documentCodeId": "770",
                        "type": "E-AANVR-TOZO",
                        "url": "focus/document?id=4400000029&isBulk=true&isDms=false",
                    },
                ],
            },
            "status": "OK",
        }

        response_json = response.json

        self.assertTrue(
            response_json["content"]["stadspassaldo"]["stadspassen"][0]["budgets"][0][
                "urlTransactions"
            ].startswith("/api/focus/stadspastransacties/")
        )

        # remove url, it has a timebased factor in it.
        del response_json["content"]["stadspassaldo"]["stadspassen"][0]["budgets"][0][
            "urlTransactions"
        ]

        del response_json["content"]["stadspassaldo"]["stadspassen"][1]["budgets"][0][
            "urlTransactions"
        ]

        del response_json["content"]["stadspassaldo"]["stadspassen"][2]["budgets"][0][
            "urlTransactions"
        ]

        self.assertEqual(response_json, expected)
