from email.mime import application
import logging
from urllib.error import HTTPError

import sentry_sdk
from flask import Flask, request, make_response
from sentry_sdk.integrations.flask import FlaskIntegration
from app.focus_service_aanvragen import (
    get_aanvragen,
)
from app.focus_service_e_aanvraag import get_e_aanvragen
from app.focus_service_get_document import get_document
from app.focus_service_specificaties import get_jaaropgaven, get_uitkeringsspecificaties
from app.focus_service_stadspas_admin import get_stadspas_admin_number

from app.gpass_service import get_stadspassen, get_transactions
from app.utils import (
    decrypt,
    error_response_json,
    get_bsn_from_request,
    success_response_json,
    validate_openapi,
    verify_tma_user,
)

from app.config import (
    API_BASE_PATH,
    IS_DEV,
    SENTRY_DSN,
    CustomJSONEncoder,
    TMAException,
)
from app.focus_config import (
    FOCUS_DOCUMENT_PATH,
)

application = Flask(__name__)
application.json_encoder = CustomJSONEncoder

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[FlaskIntegration()], with_locals=False
    )


@application.route("/status/health", methods=["GET"])
def status_health():
    return success_response_json("OK")


@application.route(f"{API_BASE_PATH}/uitkering-en-stadspas/aanvragen", methods=["GET"])
@verify_tma_user
@validate_openapi
def aanvragen():
    bsn = get_bsn_from_request()
    aanvragen = get_aanvragen(bsn)
    return success_response_json(aanvragen)


@application.route(f"{API_BASE_PATH}/e-aanvragen", methods=["GET"])
@verify_tma_user
@validate_openapi
def e_aanvragen():
    bsn = get_bsn_from_request()
    aanvragen = get_e_aanvragen(bsn)
    return success_response_json(aanvragen)


@application.route(f"/{FOCUS_DOCUMENT_PATH}", methods=["GET"])
@verify_tma_user
@validate_openapi
def document():
    bsn = get_bsn_from_request()
    id = request.args.get("id", None)
    isBulk = request.args.get("isBulk", "false").lower() == "true"
    isDms = request.args.get("isDms", "false").lower() == "true"

    document = get_document(bsn, id, isBulk, isDms)
    response = make_response(document["document_content"])

    headers = {
        "Content-Disposition": f'attachment; filename="{document["file_name"]}"',
        "Content-Type": document["mime_type"],
    }

    response.headers = headers

    return response


@application.route(
    f"{API_BASE_PATH}/uitkering/specificaties-en-jaaropgaven", methods=["GET"]
)
@verify_tma_user
@validate_openapi
def specificaties_en_jaaropgaven():
    bsn = get_bsn_from_request()
    jaaropgaven = get_jaaropgaven(bsn)
    uitkeringsspecificaties = get_uitkeringsspecificaties(bsn)
    response_content = {
        "jaaropgaven": jaaropgaven,
        "uitkeringsspecificaties": uitkeringsspecificaties,
    }
    return success_response_json(response_content)


@application.route(f"{API_BASE_PATH}/stadspas", methods=["GET"])
@verify_tma_user
@validate_openapi
def stadspassen():
    bsn = get_bsn_from_request()
    admin = get_stadspas_admin_number(bsn)

    if not admin["admin_number"]:
        return success_response_json(None)

    stadspassen = get_stadspassen(admin["admin_number"])
    response_content = {
        "stadspassen": stadspassen,
        "adminNumber": admin["admin_number"],
        "ownerType": admin["type"],
    }

    return success_response_json(response_content)


@application.route(
    f"{API_BASE_PATH}/stadspas/transacties/<string:encrypted_admin_pasnummer>",
    methods=["GET"],
)
@verify_tma_user
@validate_openapi
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
