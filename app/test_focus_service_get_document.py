import base64
from unittest import TestCase
from unittest.mock import call, patch
from app.focus_service_get_document import get_document


example_soap_response = {
    "contentID": None,
    "contentLanguage": [],
    "contentMD5": None,
    "dataHandler": b"document-content",
    "description": None,
    "disposition": "attachment",
    "document": None,
    "fileName": "Aanvraag Stadspas (balie).pdf",
}


class FocusSerivceGetDocumentTest(TestCase):
    # @patch("app.focus_service_e_aanvraag.logging.error")
    @patch("app.focus_service_get_document.send_document_request")
    def test_get_document(self, send_document_request_mock):

        send_document_request_mock.return_value = example_soap_response

        bsn = "123xx123"
        doc_id = "123"
        is_dms = False
        is_bulk = False

        result = get_document(bsn, doc_id, is_bulk, is_dms)

        send_document_request_mock.assert_called_with(
            bsn, doc_id, is_bulk, is_dms, raw_response=False
        )

        result_expected = {
            "file_name": "Aanvraag Stadspas (balie).pdf",
            "document_content": b"document-content",
            "mime_type": "application/pdf",
        }

        self.assertEqual(result, result_expected)

    @patch("app.focus_service_get_document.send_document_request")
    def test_get_document_other_mimetype(self, send_document_request_mock):

        send_document_request_mock.return_value = {
            **example_soap_response,
            "fileName": "testding",
        }

        bsn = "123xx123"
        doc_id = "123"
        is_dms = False
        is_bulk = False

        result = get_document(bsn, doc_id, is_bulk, is_dms)

        send_document_request_mock.assert_called_with(
            bsn, doc_id, is_bulk, is_dms, raw_response=False
        )

        result_expected = {
            "file_name": "testding",
            "document_content": b"document-content",
            "mime_type": "application/octet-stream",
        }

        self.assertEqual(result, result_expected)

    @patch("app.focus_service_get_document.send_document_request")
    def test_get_document_fallback(self, send_document_request_mock):

        send_document_request_mock.side_effect = [
            {},
            {
                **example_soap_response,
                "dataHandler": base64.b64encode(b"document-content").decode(),
            },
        ]

        bsn = "123xx123"
        doc_id = "123"
        is_dms = False
        is_bulk = False

        result = get_document(bsn, doc_id, is_bulk, is_dms)

        send_document_request_mock.assert_has_calls(
            [
                call("123xx123", "123", False, False, raw_response=False),
                call(
                    "123xx123",
                    "123",
                    False,
                    False,
                    header_value={"Accept": "application/xop+xml"},
                    raw_response=False,
                ),
            ]
        )

        result_expected = {
            "file_name": "Aanvraag Stadspas (balie).pdf",
            "document_content": b"document-content",
            "mime_type": "application/pdf",
        }

        self.assertEqual(result, result_expected)

    @patch("app.focus_service_get_document.send_document_request")
    def test_get_document_empty(self, send_document_request_mock):

        send_document_request_mock.side_effect = [
            {},
            {},
        ]

        bsn = "123xx123"
        doc_id = "123"
        is_dms = False
        is_bulk = False

        self.assertRaises(Exception, get_document, bsn, doc_id, is_bulk, is_dms)

        send_document_request_mock.assert_has_calls(
            [
                call("123xx123", "123", False, False, raw_response=False),
                call(
                    "123xx123",
                    "123",
                    False,
                    False,
                    header_value={"Accept": "application/xop+xml"},
                    raw_response=False,
                ),
            ]
        )

    @patch("app.focus_service_get_document.send_document_request")
    def test_get_document_call_fails(self, send_document_request_mock):

        send_document_request_mock.return_value = None

        bsn = "123xx123"
        doc_id = "123"
        is_dms = False
        is_bulk = False

        self.assertRaises(Exception, get_document, bsn, doc_id, is_bulk, is_dms)

        send_document_request_mock.assert_called()
