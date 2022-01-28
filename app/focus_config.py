import os

# Focus
FOCUS_WSDL = os.getenv("FOCUS_WSDL")
FOCUS_CERTIFICATE = os.getenv("FOCUS_CERTIFICATE", False)
FOCUS_USERNAME = os.getenv("FOCUS_USERNAME")
FOCUS_PASSWORD = os.getenv("FOCUS_PASSWORD")

FOCUS_DOCUMENT_PATH = "wpi/aanvraag/document"

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