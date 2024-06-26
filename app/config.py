import locale
import logging
import os
from datetime import date, datetime, time

from flask.json.provider import DefaultJSONProvider

locale.setlocale(locale.LC_TIME, "nl_NL.UTF-8")

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

OTAP_ENV = os.getenv("MA_OTAP_ENV")

# Environment determination
IS_PRODUCTION = OTAP_ENV == "production"
IS_ACCEPTANCE = OTAP_ENV == "acceptance"
IS_DEV = OTAP_ENV == "development"
IS_TEST = OTAP_ENV == "test"

IS_TAP = IS_PRODUCTION or IS_ACCEPTANCE or IS_TEST
IS_AP = IS_ACCEPTANCE or IS_PRODUCTION
IS_OT = IS_DEV or IS_TEST
IS_AZ = os.getenv("IS_AZ", False)

# App constants
VERIFY_JWT_SIGNATURE = os.getenv("VERIFY_JWT_SIGNATURE", IS_AP)
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


class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, time):
            return obj.isoformat(timespec="minutes")

        if isinstance(obj, date):
            return obj.isoformat()

        return super().default(obj)


def get_application_insights_connection_string():
    return os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", None)
