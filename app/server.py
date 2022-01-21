from email.mime import application

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from app.config import get_TMA_certificate
from app.utils import decrypt, get_bsn_from_request
from app.gpass_service import get_transactions

from .config_new import (
    SENTRY_DSN,
    CustomJSONEncoder,
    focus_credentials,
    urls,
    zeep_config,
)
from .focusconnect import FocusConnection
from .focusserver import FocusServer

application = Flask(__name__)
application.json_encoder = CustomJSONEncoder

if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[FlaskIntegration()], with_locals=False
    )


def get_server():
    focus_connection = FocusConnection(zeep_config, focus_credentials)
    return FocusServer(focus_connection, get_TMA_certificate())


@application.route(urls["health"])
def status_health():
    return get_server().health()


@application.route(urls["data"])
def status_data():
    return get_server().status_data()


@application.route(urls["aanvragen"])
def aanvragen():
    bsn = get_bsn_from_request()
    return get_server().aanvragen(bsn)


@application.route(urls["document"])
def document():
    bsn = get_bsn_from_request()
    return get_server().document(bsn)


@application.route(urls["combined"])
def combined():
    bsn = get_bsn_from_request()
    return get_server().combined(bsn)


@application.route(urls["stadspastransacties"])
def stadspastransactions(encrypted_admin_pasnummer):
    budget_code, admin_number, stadspas_number = decrypt(encrypted_admin_pasnummer)

    stadspas_transations = get_transactions(admin_number, stadspas_number, budget_code)
    if stadspas_transations is None:
        return {}, 204

    return {
        "status": "ok",
        "content": stadspas_transations,
    }


if __name__ == "__main__":
    application.run()
