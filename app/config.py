import locale
import logging
import os
from datetime import date, time
from json import JSONEncoder

locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# Sentry configuration.
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_ENV = os.getenv("SENTRY_ENVIRONMENT")

# Environment determination
IS_PRODUCTION = SENTRY_ENV == "production"
IS_ACCEPTANCE = SENTRY_ENV == "acceptance"
IS_AP = IS_PRODUCTION or IS_ACCEPTANCE
IS_DEV = os.getenv("FLASK_ENV") == "development" and not IS_AP

# Server security / certificates for ZorgNed
SERVER_CLIENT_CERT = os.getenv("MIJN_DATA_CLIENT_CERT")
SERVER_CLIENT_KEY = os.getenv("MIJN_DATA_CLIENT_KEY")

# ZorgNed vars
ZORGNED_STADSPASSEN_ENABLED = not IS_PRODUCTION
ZORGNED_API_REQUEST_TIMEOUT_SECONDS = 30
ZORGNED_API_TOKEN = os.getenv("WMO_NED_API_TOKEN")
ZORGNED_API_URL = os.getenv("ZORGNED_API_URL")
ZORGNED_GEMEENTE_CODE = "0363"


# App constants
ENABLE_OPENAPI_VALIDATION = os.getenv("ENABLE_OPENAPI_VALIDATION", not IS_AP)

API_REQUEST_TIMEOUT = 30
API_BASE_PATH = "/wpi"

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


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.isoformat(timespec="minutes")
        if isinstance(obj, date):
            return obj.isoformat()

        return JSONEncoder.default(self, obj)
