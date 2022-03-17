import base64
from app.focus_service_aanvragen import get_client


def send_document_request(bsn, id, isBulk, isDms, header_value={}, raw_response=False):
    client = get_client()
    with client.settings(extra_http_headers=header_value, raw_response=raw_response):
        document = client.service.getDocument(
            id=id,
            bsn=bsn,
            isBulk=isBulk,
            isDms=isDms,
        )
        return document


def get_document(bsn, id, isBulk, isDms, raw_response=False):

    document_content = None

    # First try to get doc without special header
    document = send_document_request(bsn, id, isBulk, isDms, raw_response=raw_response)

    if raw_response and document:
        return document

    if document is None:
        raise Exception("Requested document is empty")

    data_handler = (
        document["dataHandler"] if document and document["dataHandler"] else None
    )

    if not data_handler:
        # Try again with the header
        document = send_document_request(
            bsn,
            id,
            isBulk,
            isDms,
            header_value={"Accept": "application/xop+xml"},
            raw_response=raw_response,
        )

        if raw_response and document:
            return document

        if document and "dataHandler" in document and document["dataHandler"]:
            document_content = base64.b64decode(document["dataHandler"])
        else:
            raise Exception("Requested document is empty")
    else:
        document_content = document["dataHandler"]

    mime_type = (
        "application/pdf"
        if ".pdf" in document["fileName"]
        else "application/octet-stream"
    )

    document = {
        "file_name": document["fileName"],
        "document_content": document_content,
        "mime_type": mime_type,
    }

    return document
