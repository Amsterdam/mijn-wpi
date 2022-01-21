from email.mime import application
import logging
from urllib.error import HTTPError

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from app.gpass_service import get_transactions
from app.utils import (
    decrypt,
    error_response_json,
    get_bsn_from_request,
    success_response_json,
)

from app.config import (
    FOCUS_DOCUMENT_PATH,
    IS_DEV,
    SENTRY_DSN,
    CustomJSONEncoder,
    TMAException,
    focus_credentials,
    zeep_config,
)
from app.focusconnect import FocusConnection
from app.focusserver import FocusServer

application = Flask(__name__)
application.json_encoder = CustomJSONEncoder

if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[FlaskIntegration()], with_locals=False
    )


def get_server():
    focus_connection = FocusConnection(zeep_config, focus_credentials)
    return FocusServer(focus_connection)


@application.route("/status/health")
def status_health():
    return success_response_json("OK")


@application.route("/focus/aanvragen")
def aanvragen():
    bsn = get_bsn_from_request()
    return get_server().aanvragen(bsn)


@application.route(f"/{FOCUS_DOCUMENT_PATH}")
def document():
    bsn = get_bsn_from_request()
    return get_server().document(bsn)


@application.route("/focus/combined")
def combined():
    bsn = get_bsn_from_request()
    combined_response_data = get_server().combined(bsn)
    return success_response_json(combined_response_data)


@application.route("/focus/stadspastransacties/<string:encrypted_admin_pasnummer>")
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
