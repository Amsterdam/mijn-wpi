import logging

from flask import Flask, send_from_directory
from flask_cors import CORS

from focus.config import check_env, config, credentials, urls, get_TMA_certificate
from focus.focusconnect import FocusConnection
from focus.focusserver import FocusServer
from flask_limiter import Limiter


def global_limiter():
    return "global_limiter"


application = Flask(__name__)
limiter = Limiter(
    application,
    key_func=global_limiter,
    default_limits=["5 per 1 second"]
)

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
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
@application.route(urls["external_health"])
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
