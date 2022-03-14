import json
import os

from app.config import API_BASE_PATH, IS_ACCEPTANCE

# Focus
FOCUS_WSDL = os.getenv("FOCUS_WSDL")
FOCUS_CERTIFICATE = os.getenv("FOCUS_CERTIFICATE", False)
FOCUS_USERNAME = os.getenv("FOCUS_USERNAME")
FOCUS_PASSWORD = os.getenv("FOCUS_PASSWORD")

FOCUS_DOCUMENT_PATH = f"{API_BASE_PATH[1:]}/document"

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
}

FOCUS_STADSPAS_FONDSEN_GROENE_STIP = [3555, 3556, 3557, 3558]
FOCUS_STADSPAS_TYPE_PER_FONDS = {
    3555: "hoofdpashouder",
    3556: "partner",
    3557: "kind",
}

FOCUS_STADSPAS_ADMIN_NUMBER_CONVERSION_ACC = (
    json.loads(os.getenv("FOCUS_STADSPAS_ADMIN_NUMBER_CONVERSION_ACC", "null"))
    if IS_ACCEPTANCE
    else None
)

zeep_config = {"wsdl": FOCUS_WSDL, "session_verify": FOCUS_CERTIFICATE}

focus_credentials = {
    "username": FOCUS_USERNAME,
    "password": FOCUS_PASSWORD,
}
