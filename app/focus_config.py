import json
import os

from app.config import API_BASE_PATH

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
    # Requirements Document Thema Inkomen Versie 4.2 / Bijlage 11 Lijst overige documenten
    # Titels gebruikt als E_AANVRAAG configuratie
    "Formulier Inlichtingen Klant": "Brief meer informatie",
    "Formulier Inlichtingen partner": "Brief meer informatie",
    "Aanvraagformulier WWB (kort)": "Brief meer informatie",
    "Aanvraag WWB (GALO)": "Aanvraag uitkering",
    "Toekenning Levensonderhoud": "Besluit toekenning",
    "Afwijzen Levensonderhoud": "Besluit afwijzing",
    "Afwijzen Levensonderhoud (BIJ)": "Besluit afwijzing",
    "Toekennen Levensonderhoud (BIJ)": "Besluit toekenning",
    "Niet in behandeling nemen": "Besluit buiten behandeling",
    # Product name
    "Levensonderhoud": "Bijstandsuitkering",
}

# NOTE: MUST Keep in this order
FOCUS_AANVRAAG_PROCESS_STEPS = [
    "aanvraag",
    "inBehandeling",
    "herstelTermijn",
    "beslissing",  # Is transformed to besluit
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

zeep_config = {"wsdl": FOCUS_WSDL, "session_verify": FOCUS_CERTIFICATE}

focus_credentials = {
    "username": FOCUS_USERNAME,
    "password": FOCUS_PASSWORD,
}
