import base64
import locale
import logging
import os
from datetime import date, time, datetime
import tempfile
from flask.json.provider import DefaultJSONProvider

locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Sentry configuration.
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_ENV = os.getenv("SENTRY_ENVIRONMENT")

# Environment determination
IS_PRODUCTION = SENTRY_ENV == "production"
IS_ACCEPTANCE = SENTRY_ENV == "acceptance"
IS_DEV = SENTRY_ENV == "development"
IS_TEST = SENTRY_ENV == "test"

IS_TAP = IS_PRODUCTION or IS_ACCEPTANCE or IS_TEST
IS_AP = IS_ACCEPTANCE or IS_PRODUCTION
IS_OT = IS_DEV or IS_TEST
IS_AZ = os.getenv("IS_AZ", False)

# App constants
VERIFY_JWT_SIGNATURE = os.getenv("VERIFY_JWT_SIGNATURE", IS_AP)
API_REQUEST_TIMEOUT = 30
API_BASE_PATH = "/wpi"

# Server security / certificates for ZorgNed
SERVER_CLIENT_CERT = os.getenv("MIJN_DATA_CLIENT_CERT")
SERVER_CLIENT_KEY = os.getenv("MIJN_DATA_CLIENT_KEY")

# TODO: Add other AZ env conditions after migration.
if IS_AZ and IS_TAP and SERVER_CLIENT_CERT is not None:
    # https://stackoverflow.com/a/46570364/756075
    # Server security / certificates
    cert = tempfile.NamedTemporaryFile(delete=False)
    cert.write(base64.b64decode(SERVER_CLIENT_CERT))
    cert.close()

    key = tempfile.NamedTemporaryFile(delete=False)
    key.write(base64.b64decode(SERVER_CLIENT_KEY))
    key.close()

    SERVER_CLIENT_CERT = cert.name
    SERVER_CLIENT_KEY = key.name

# ZorgNed vars
ZORGNED_STADSPASSEN_ENABLED = True
ZORGNED_API_REQUEST_TIMEOUT_SECONDS = 30
ZORGNED_API_TOKEN = os.getenv("ZORGNED_API_TOKEN")
ZORGNED_API_URL = os.getenv("ZORGNED_API_URL")
ZORGNED_GEMEENTE_CODE = "0363"

# Set-up logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").upper()
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d in function %(funcName)s] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=LOG_LEVEL,
)


CONNECTION_ERRORS = [
    "Max retries exceeded with url",
    "Failed to establish a connection",
    "Connection aborted",
    "read timeout",
    "ConnectionError",
]


class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, time):
            return obj.isoformat(timespec="minutes")

        if isinstance(obj, date):
            return obj.isoformat()

        return super().default(obj)
