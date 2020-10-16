import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask, send_from_directory
from flask_cors import CORS

from focus.gpass_connect import GpassConnection

from focus.crypto import decrypt
from .config import check_env, config, credentials, urls, get_TMA_certificate, SENTRY_DSN, get_gpass_bearer_token, \
    get_gpass_api_location
from .focusconnect import FocusConnection
from .focusserver import FocusServer
from flask_limiter import Limiter


def global_limiter():
    return "global_limiter"


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        with_locals=False
    )


application = Flask(__name__)
limiter = Limiter(
    application,
    key_func=global_limiter,
    default_limits=["5 per 1 second"]
)


logger = logging.getLogger(__name__)

log_handler = logging.StreamHandler()
application.logger.addHandler(log_handler)

CORS(app=application, send_wildcard=True)

# Main
# Check the environment, will raise an exception if the server is not supplied with sufficient info
check_env()
# Initialize server to None, instantiate on first call to focus_server
focus_server = None


def server():
    """
    Gets a server to execute the request.
    If the server is not alive (failing connection) a new server is created automatically
    :return:
    """
    global focus_server
    if focus_server is None or not focus_server.is_alive():
        # Establish a (new) connection with the FOCUS system
        focus_connection = FocusConnection(config, credentials)
        # Serve the FOCUS requests that are exposed by this server
        focus_server = FocusServer(focus_connection, get_TMA_certificate())
    return focus_server


@application.route(urls["swagger"])
def swagger_yaml():
    return send_from_directory('static', 'swagger.yaml')


@application.route(urls["health"])
@limiter.exempt
def status_health():
    return server().health()


@application.route(urls["data"])
@limiter.exempt
def status_data():
    return server().status_data()


@application.route(urls["aanvragen"])
def aanvragen():
    return server().aanvragen()


@application.route(urls["document"])
def document():
    return server().document()


@application.route(urls["combined"])
def combined():
    return server().combined()


@application.route(urls["stadspastransacties"])
def stadspastransactions(encrypted_admin_pasnummer):
    admin_number, stadspas_number = decrypt(encrypted_admin_pasnummer)

    gpass_con = GpassConnection(get_gpass_api_location(), get_gpass_bearer_token())
    stadspas_transations = gpass_con.get_transactions(admin_number, stadspas_number)
    if stadspas_transations is None:
        return {}, 204

    return {
        "status": "ok",
        "content": stadspas_transations,
    }


if __name__ == "__main__":
    application.run()
