import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask, send_from_directory
from flask_cors import CORS

from .config import check_env, config, credentials, urls, get_TMA_certificate, SENTRY_DSN
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
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('focus/logs/app.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

log_handler = logging.StreamHandler()

application.logger.addHandler(log_handler)
application.logger.addHandler(file_handler)

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


@application.route(urls["log"])
def app_log():
    return send_from_directory('logs', 'app.log')


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


if __name__ == "__main__":
    application.run()
