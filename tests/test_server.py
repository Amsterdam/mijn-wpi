import json
from mock import patch

from app.tests.wpi_test_app import WpiApiTestApp
from tests.mocks import MockClient

# side step decoding the BSN from SAML token
@patch("app.server.get_bsn_from_request", lambda: 123456789)
@patch("app.focusconnect.Client", new=MockClient)
@patch("app.gpass_service.GPASS_API_LOCATION", "http://localhost")
@patch("app.utils.GPASS_FERNET_ENCRYPTION_KEY", "abcde1234")
class TestApi(WpiApiTestApp):

    TESTKEY = "z4QXWk3bjwFST2HRRVidnn7Se8VFCaHscK39JfODzNs="

    # @patch(
    #     "app.focusconnect.FocusConnection.aanvragen",
    #     new=lambda s, bsn, url_root: {"aap": "noot"},
    # )
    # def test_verhuizingen_with_connection(self):
    #     """
    #     Expect a result with meldingen
    #     """
    #     response = self.client.get("/focus/aanvragen")
    #     self.assertEqual(response.status_code, 200)
    #     result = json.loads(response.data)
    #     self.assertEqual(result["aap"], "noot")

    # def test_health(self):
    #     """
    #     Simple respond OK when the API is up
    #     :return:
    #     """
    #     response = self.client.get("/status/health")
    #     self.assertEqual(response.status_code, 200)

    # @patch("app.gpass_service.get_stadspassen")
    # def test_combined_api(self, get_stadspassen_mock):

    #     get_stadspassen_mock.return_value = []

    #     response = self.client.get("/focus/combined")

    #     response_json = response.json

    #     self.assertTrue(
    #         response_json["content"]["stadspassaldo"]["stadspassen"][0]["budgets"][0][
    #             "urlTransactions"
    #         ].startswith("/api/focus/stadspastransacties/")
    #     )

    #     # remove url, it has a timebased factor in it.
    #     del response_json["content"]["stadspassaldo"]["stadspassen"][0]["budgets"][0][
    #         "urlTransactions"
    #     ]

    #     del response_json["content"]["stadspassaldo"]["stadspassen"][1]["budgets"][0][
    #         "urlTransactions"
    #     ]

    #     del response_json["content"]["stadspassaldo"]["stadspassen"][2]["budgets"][0][
    #         "urlTransactions"
    #     ]

    #     self.assertEqual(response_json, expected)
