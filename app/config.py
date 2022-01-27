from datetime import date, time
from json import JSONEncoder
import os
import logging

from tma_saml.exceptions import (
    InvalidBSNException,
    SamlExpiredException,
    SamlVerificationException,
)

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

TMA_CERTIFICATE = os.getenv("TMA_CERTIFICATE")

# Sentry configuration.
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_ENV = os.getenv("SENTRY_ENVIRONMENT")

# Environment determination
IS_PRODUCTION = SENTRY_ENV == "production"
IS_ACCEPTANCE = SENTRY_ENV == "acceptance"
IS_AP = IS_PRODUCTION or IS_ACCEPTANCE
IS_DEV = os.getenv("FLASK_ENV") == "development" and not IS_AP
IS_AP = IS_PRODUCTION or IS_ACCEPTANCE
IS_DEV = os.getenv("FLASK_ENV") == "development" and not IS_AP

# App constants
TMAException = (SamlVerificationException, InvalidBSNException, SamlExpiredException)
ENABLE_OPENAPI_VALIDATION = os.getenv("ENABLE_OPENAPI_VALIDATION", "1")

API_REQUEST_TIMEOUT = 30

# Focus
FOCUS_WSDL = os.getenv("FOCUS_WSDL")
FOCUS_CERTIFICATE = os.getenv("FOCUS_CERTIFICATE", False)
FOCUS_USERNAME = os.getenv("FOCUS_USERNAME")
FOCUS_PASSWORD = os.getenv("FOCUS_PASSWORD")

FOCUS_DOCUMENT_PATH = "focus/document"

FOCUS_PRODUCTS_ALLOWED = ["Levensonderhoud", "Stadspas"]
FOCUS_PRODUCT_GROUPS_ALLOWED = ["Minimafonds", "Participatiewet"]

# NOTE: We probably need more up-to-date translations.
FOCUS_TITLE_TRANSLATIONS = {
    # Document titles
    "LO: Aanvraag": "Aanvraag bijstandsuitkering",
    "LO: Besluit": "Besluit aanvraag bijstandsuitkering",
    "LO: In behandeling": "Uw aanvraag is in behandeling genomen",
    "LO: Herstel": "Verzoek om aanvullende informatie van u",
    # Product name
    "Levensonderhoud": "Bijstandsuitkering",
}

# NOTE: MUST Keep in this order
FOCUS_AANVRAAG_PROCESS_STEPS = [
    "aanvraag",
    "inBehandeling",
    "herstelTermijn",
    "beslissing",
]

FOCUS_STEP_ID_TRANSLATIONS = {
    # Stadspas / Bijstandsuitkering
    "aanvraag": "Aanvraag",
    "inBehandeling": "In behandeling",
    "herstelTermijn": "Informatie nodig",
    "besluit": "Besluit",
    # Tozo / Tonk / Bbz
    "terugvorderingsbesluit": "Terugvorderings- besluit",
    "inkomstenwijziging": "Wijziging inkomsten",
    "bezwaar": "Bezwaar",
    "brief": "Brief",
    "mail": "Mail",
    "voorschot": "Voorschot",
    "tijdNodig": "Tijd nodig",
    "akte": "Akte",
}

zeep_config = {"wsdl": FOCUS_WSDL, "session_verify": FOCUS_CERTIFICATE}

focus_credentials = {
    "username": FOCUS_USERNAME,
    "password": FOCUS_PASSWORD,
}

# GPASS
GPASS_API_TOKEN = os.getenv("GPASS_TOKEN")
GPASS_API_LOCATION = os.getenv("GPASS_API_LOCATION")
GPASS_FERNET_ENCRYPTION_KEY = os.getenv("FERNET_KEY")

# Set-up logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").upper()
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d in function %(funcName)s] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=LOG_LEVEL,
)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.isoformat(timespec="minutes")
        if isinstance(obj, date):
            return obj.isoformat()

        return JSONEncoder.default(self, obj)
