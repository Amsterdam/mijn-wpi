from email.mime import application
import logging
from urllib.error import HTTPError

import sentry_sdk
from flask import Flask, request, make_response
from sentry_sdk.integrations.flask import FlaskIntegration
from app.focus_service_aanvragen import (
    get_aanvragen,
)
from app.focus_service_get_document import get_document
from app.focus_service_stadspas_admin import get_stadspas_admin_number

from app.gpass_service import get_stadspassen, get_transactions
from app.utils import (
    decrypt,
    error_response_json,
    get_bsn_from_request,
    success_response_json,
)

from app.config import (
    IS_DEV,
    SENTRY_DSN,
    CustomJSONEncoder,
    TMAException,
)
from app.focus_config import (
    FOCUS_DOCUMENT_PATH,
)

# from app.focusconnect import FocusConnection
# from app.focusserver import FocusServer

application = Flask(__name__)
application.json_encoder = CustomJSONEncoder

if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[FlaskIntegration()], with_locals=False
    )


@application.route("/status/health")
def status_health():
    return success_response_json("OK")


@application.route("/sociaal/aanvragen")
def aanvragen():
    bsn = get_bsn_from_request()
    aanvragen = get_aanvragen(bsn)

    return success_response_json(aanvragen)


@application.route(f"/{FOCUS_DOCUMENT_PATH}")
def document():
    bsn = get_bsn_from_request()
    id = request.args.get("id", None)
    isBulk = request.args.get("isBulk", "false").lower() == "true"
    isDms = request.args.get("isDms", "false").lower() == "true"

    document = get_document(bsn, id, isBulk, isDms)

    response = make_response(document["document_content"])
    response.headers[
        "Content-Disposition"
    ] = f'attachment; filename="{document["file_name"]}"'
    response.headers["Content-Type"] = document["mime_type"]

    return response


@application.route("/wpi/bijstanduitkering/jaaropgaven")
def jaaropgaven():
    bsn = get_bsn_from_request()
    jaaropgaven = []
    return success_response_json(jaaropgaven)


@application.route("/wpi/bijstanduitkering/specificaties")
def uitkeringspecificaties():
    bsn = get_bsn_from_request()
    uitkeringspecificaties = []
    return success_response_json(uitkeringspecificaties)


@application.route("/wpi/stadspassen")
def stadspassen():
    bsn = get_bsn_from_request()
    admin_number = get_stadspas_admin_number(bsn)
    stadspassen = get_stadspassen(admin_number)
    return success_response_json(stadspassen)


@application.route("/wpi/stadspas/transacties/<string:encrypted_admin_pasnummer>")
def stadspastransactions(encrypted_admin_pasnummer):
    budget_code, admin_number, stadspas_number = decrypt(encrypted_admin_pasnummer)
    stadspas_transations = get_transactions(admin_number, stadspas_number, budget_code)
    return success_response_json(stadspas_transations)


@application.errorhandler(Exception)
def handle_error(error):

    error_message_original = str(error)

    msg_tma_exception = "TMA error occurred"
    msg_request_http_error = "Request error occurred"
    msg_server_error = "Server error occurred"

    logging.exception(error, extra={"error_message_original": error_message_original})

    if IS_DEV:
        msg_tma_exception = error_message_original
        msg_request_http_error = error_message_original
        msg_server_error = error_message_original

    if isinstance(error, HTTPError):
        return error_response_json(
            msg_request_http_error,
            error.response.status_code,
        )
    elif isinstance(error, TMAException):
        return error_response_json(msg_tma_exception, 400)

    return error_response_json(msg_server_error, 500)


if __name__ == "__main__":
    application.run()
