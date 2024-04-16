import logging
import os
from urllib.error import HTTPError

from flask import Flask, Response, request

from app import auth
from app.config import API_BASE_PATH, IS_OT, UpdatedJSONProvider
from app.focus_config import FOCUS_DOCUMENT_PATH
from app.focus_service_aanvragen import get_aanvragen
from app.focus_service_e_aanvraag import get_e_aanvragen
from app.focus_service_get_document import get_document
from app.focus_service_specificaties import get_jaaropgaven, get_uitkeringsspecificaties
from app.utils import error_response_json, success_response_json

application = Flask(__name__)
application.json = UpdatedJSONProvider(application)


@application.route("/")
@application.route("/status/health")
def health_check():
    return success_response_json(
        {
            "gitSha": os.getenv("MA_GIT_SHA", -1),
            "buildId": os.getenv("MA_BUILD_ID", -1),
            "otapEnv": os.getenv("MA_OTAP_ENV", None),
        }
    )


@application.route(f"{API_BASE_PATH}/uitkering/aanvragen", methods=["GET"])
@auth.login_required
def aanvragen():
    user = auth.get_current_user()
    aanvragen = get_aanvragen(user["id"])
    return success_response_json(aanvragen)


@application.route(f"{API_BASE_PATH}/e-aanvragen", methods=["GET"])
@auth.login_required
def e_aanvragen():
    user = auth.get_current_user()
    aanvragen = get_e_aanvragen(user["id"])
    return success_response_json(aanvragen)


@application.route(f"/{FOCUS_DOCUMENT_PATH}", methods=["GET"])
@auth.login_required
def document():
    user = auth.get_current_user()
    id = request.args.get("id", None)
    isBulk = request.args.get("isBulk", "false").lower() == "true"
    isDms = request.args.get("isDms", "false").lower() == "true"

    document = get_document(user["id"], id, isBulk, isDms)

    response = Response(
        response=document["document_content"],
        headers={
            "Content-Disposition": f'attachment; filename="{document["file_name"]}"',
            "Content-Type": document["mime_type"],
        },
        mimetype=document["mime_type"],
    )

    return response


@application.route(
    f"{API_BASE_PATH}/uitkering/specificaties-en-jaaropgaven", methods=["GET"]
)
@auth.login_required
def specificaties_en_jaaropgaven():
    user = auth.get_current_user()
    jaaropgaven = get_jaaropgaven(user["id"])
    uitkeringsspecificaties = get_uitkeringsspecificaties(user["id"])
    response_content = {
        "jaaropgaven": jaaropgaven,
        "uitkeringsspecificaties": uitkeringsspecificaties,
    }
    return success_response_json(response_content)


@application.errorhandler(Exception)
def handle_error(error):
    error_message_original = f"{type(error)}:{str(error)}"

    msg_auth_exception = "Auth error occurred"
    msg_request_http_error = "Request error occurred"
    msg_server_error = "Server error occurred"

    logging.exception(error, extra={"error_message_original": error_message_original})

    if IS_OT:  # pragma: no cover
        msg_auth_exception = error_message_original
        msg_request_http_error = error_message_original
        msg_server_error = error_message_original

    if isinstance(error, HTTPError):
        return error_response_json(
            msg_request_http_error,
            error.response.status_code,
        )
    elif auth.is_auth_exception(error):
        return error_response_json(msg_auth_exception, 401)

    return error_response_json(
        msg_server_error,
        msg_server_error,
        error.code if hasattr(error, "code") else 500,
    )


if __name__ == "__main__":  # pragma: no cover
    application.run()
