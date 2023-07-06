from app.e_aanvraag_specificaties_config import jaaropgave_document_codes

E_AANVRAAG_ABOUT = {
    "Tozo 1": "Tozo 1",
    "Tozo 2": "Tozo 2",
    "Tozo 3": "Tozo 3",
    "Tozo 4": "Tozo 4",
    "Tozo 5": "Tozo 5",
    "TONK": "TONK",
    "IOAZ": "IOAZ",
    "Bbz": "Bbz",
}

E_ABOUT_SPECIFIC_UITKERING = "uitkering"
E_ABOUT_SPECIFIC_LENING = "lening"

E_AANVRAAG_PRODUCT_TITLES = {
    E_AANVRAAG_ABOUT["Tozo 1"]: "Tozo 1 (aangevraagd voor 1 juni 2020)",
    E_AANVRAAG_ABOUT["Tozo 2"]: "Tozo 2 (aangevraagd vanaf 1 juni 2020)",
    E_AANVRAAG_ABOUT["Tozo 3"]: "Tozo 3 (aangevraagd vanaf 1 oktober 2020)",
    E_AANVRAAG_ABOUT["Tozo 4"]: "Tozo 4 (aangevraagd vanaf 1 april 2021)",
    E_AANVRAAG_ABOUT["Tozo 5"]: "Tozo 5 (aangevraagd vanaf 1 juli 2021)",
    E_AANVRAAG_ABOUT["TONK"]: "TONK",
    E_AANVRAAG_ABOUT["Bbz"]: "Bbz",
}

E_AANVRAAG_STEP_COLLECTION_IDS = list(E_AANVRAAG_PRODUCT_TITLES.keys())

E_AANVRAAG_STEP_ID = {
    "aanvraag": "aanvraag",
    "beslisTermijn": "beslisTermijn",
    "besluit": "besluit",
    "briefAdviesRapport": "briefAdviesRapport",
    "briefAkteBedrijfskapitaal": "briefAkteBedrijfskapitaal",
    "briefWeigering": "briefWeigering",
    "correctiemail": "correctiemail",
    "herstelTermijn": "herstelTermijn",
    "inkomstenwijziging": "inkomstenwijziging",
    "intrekking": "intrekking",
    "terugvorderingsbesluit": "terugvorderingsbesluit",
    "voorschot": "voorschot",
    "informatieOntvangen": "informatieOntvangen"
}

E_AANVRAAG_STEP_ID_TRANSLATIONS = {
    E_AANVRAAG_STEP_ID["aanvraag"]: "Aanvraag",
    E_AANVRAAG_STEP_ID["besluit"]: "Besluit",
    E_AANVRAAG_STEP_ID["herstelTermijn"]: "Informatie nodig",
    E_AANVRAAG_STEP_ID["intrekking"]: "Brief",
    # Tozo 1-5 / Bbz
    E_AANVRAAG_STEP_ID["voorschot"]: "Voorschot",
    E_AANVRAAG_STEP_ID["terugvorderingsbesluit"]: "Terugvorderings- besluit",
    # Tozo 1-5 / Bbz
    E_AANVRAAG_STEP_ID["inkomstenwijziging"]: "Wijziging inkomsten",
    # Bbz
    E_AANVRAAG_STEP_ID["briefAdviesRapport"]: "Brief",
    E_AANVRAAG_STEP_ID["briefAkteBedrijfskapitaal"]: "Akte",
    E_AANVRAAG_STEP_ID["beslisTermijn"]: "Tijd nodig",
    E_AANVRAAG_STEP_ID["informatieOntvangen"]: "Informatie ontvangen",
    # TONK
    E_AANVRAAG_STEP_ID["correctiemail"]: "Mail",
    E_AANVRAAG_STEP_ID["briefWeigering"]: "Brief",
}

E_AANVRAAG_DECISION_ID = {
    "afwijzing": "afwijzing",
    "buitenBehandeling": "buitenBehandeling",
    "toekenning": "toekenning",
    # Tozo 1
    "vrijeBeschikking": "vrijeBeschikking",
    # Bbz / IOAZ
    "toekenningVoorlopig": "toekenningVoorlopig",
    "beschikking": "beschikking",
    # Tonk
    "verlenging": "verlenging",
    "mogelijkeVerlenging": "mogelijkeVerlenging",
}


exclude_documents_from_processing = list(jaaropgave_document_codes.keys())

# omschrijving: Original name of document
# document_title: Mijn Amsterdam name of document
# about: See $E_AANVRAAG_ABOUT,
# about_parent: See $E_AANVRAAG_ABOUT,
# about_specific: More specific type of about. "$about Uitkering" | "$about Lening"
# step_id: See $E_AANVRAAG_STEP_ID,
# decision: See $E_AANVRAAG_DECISION_ID
E_AANVRAAG_DOCUMENT_CONFIG = {
    # Tozo 1
    "756": {
        "omschrijving": "Verkorte Aanvraag BBZ",
        "document_title": "Aanvraag Tozo 1",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
    },
    "770": {
        "omschrijving": "Tegemoetkoming Ondernemers en Zelfstandigen",
        "document_title": "Aanvraag Tozo 1",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
    },
    "175296": {
        "omschrijving": "Toekennen voorschot Tozo",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "175299": {
        "omschrijving": "Bbz Toekennen voorschot Tozo via batch",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "175303": {
        "omschrijving": "Tozo Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "175304": {
        "omschrijving": "Tozo Afwijzen",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "175305": {
        "omschrijving": "Tozo Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
    },
    "175306": {
        "omschrijving": "Tozo Hersteltermijn",
        "document_title": "Brief meer informatie",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
    },
    "175308": {
        "omschrijving": "Tozo Terugvordering voorschot",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "175311": {
        "omschrijving": "Tozo Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "about_specific": E_ABOUT_SPECIFIC_LENING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "175314": {
        "omschrijving": "Tozo Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "175317": {
        "omschrijving": "Tozo Intrekken met terugvordering voorschot",
        "document_title": "Besluit intrekking met terugbetaling",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
    },
    "175331": {
        "omschrijving": "Tozo Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
    },
    "175334": {
        "omschrijving": "Tozo Vrije beschikking",
        "document_title": "Besluit Tozo 1 aanvraag",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["vrijeBeschikking"],
    },
    "175335": {
        "omschrijving": "Tozo Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Tozo 1"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    # TOZO 2
    "777": {
        "omschrijving": "TOZO 2 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Aanvraag Tozo 2",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
    },
    "175336": {
        "omschrijving": "Tozo2 Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "175337": {
        "omschrijving": "Tozo2 Afwijzen",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "175338": {
        "omschrijving": "Tozo2 Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "about_specific": E_ABOUT_SPECIFIC_LENING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "175340": {
        "omschrijving": "Tozo2 Hersteltermijn",
        "document_title": "Brief meer informatie",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
    },
    "175341": {
        "omschrijving": "Tozo2 Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
    },
    "175342": {
        "omschrijving": "Tozo2 Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
    },
    "175343": {
        "omschrijving": "Tozo2 Terugvordering voorschot",
        "document_title": "Besluit terugvordering",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "175344": {
        "omschrijving": "Tozo2 Intrekken met terugvordering voorschot",
        "document_title": "Besluit intrekking met terugbetaling",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
    },
    "175345": {
        "omschrijving": "Tozo2 Toekennen voorschot via batch",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "175346": {
        "omschrijving": "Tozo2 Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "175347": {
        "omschrijving": "Tozo2 Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "175359": {
        "omschrijving": "Tozo2 Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    # Na besluit
    "790": {
        "omschrijving": "Tozo 2 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": E_AANVRAAG_STEP_ID["inkomstenwijziging"],
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
    },
    "175650": {
        "omschrijving": "Tozo 2 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "175645": {
        "omschrijving": "Tozo 2 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Tozo 2"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    # TOZO 3
    "785": {
        "omschrijving": "TOZO 3 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Aanvraag Tozo 3",
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
    },
    "175309": {
        "omschrijving": "Tozo3 Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "175307": {
        "omschrijving": "Tozo3 Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
    },
    "175310": {
        "omschrijving": "Tozo3 Hersteltermijn",
        "document_title": "Brief meer informatie",
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
    },
    "175357": {
        "omschrijving": "Tozo3 Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "175358": {
        "omschrijving": "Tozo3 Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
    },
    "175364": {
        "omschrijving": "Tozo3 Afwijzen",
        "document_title": "Besluit afwijzing",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
    },
    "175367": {
        "omschrijving": "Tozo3 Intrekken met terugvordering voorschot",
        "document_title": "Besluit intrekking met terugbetaling",
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
    },
    "175368": {
        "omschrijving": "Tozo3 Terugvordering voorschot",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
    },
    "175369": {
        "omschrijving": "Tozo3 Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "about_specific": E_ABOUT_SPECIFIC_LENING,
    },
    "175370": {
        "omschrijving": "Tozo3 Intrekken",
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "document_title": "Brief intrekking aanvraag",
    },
    "175371": {
        "omschrijving": "Tozo3 Afwijzen via batch",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "document_title": "Besluit afwijzing",
    },
    "175372": {
        "omschrijving": "Tozo3 Toekennen voorschot via batch",
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "document_title": "Brief betaling voorschot",
    },
    # Na besluit
    "792": {
        "omschrijving": "Tozo 3 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": E_AANVRAAG_STEP_ID["inkomstenwijziging"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
    },
    "1725650": {
        "omschrijving": "Tozo 3 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "1725645": {
        "omschrijving": "Tozo 3 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Tozo 3"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    # TOZO 4
    "800": {
        "omschrijving": "Tozo 4 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Aanvraag Tozo 4",
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175654": {
        "omschrijving": "Tozo 4 Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "175651": {
        "omschrijving": "Tozo 4 Afwijzen",
        "document_title": "Besluit afwijzing",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175673": {
        "omschrijving": "Tozo 4 Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175656": {
        "omschrijving": "Tozo 4 Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
        "about_specific": E_ABOUT_SPECIFIC_LENING,
    },
    "175689": {
        "omschrijving": "Tozo 4 Hersteltermijn",
        "document_title": "Brief meer informatie",
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175670": {
        "omschrijving": "Tozo 4 Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175652": {
        "omschrijving": "Tozo 4 Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175677": {
        "omschrijving": "Tozo 4 Toekennen voorschot via batch",
        "document_title": "Brief betaling voorschot",
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175657": {
        "omschrijving": "Tozo 4 Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "175674": {
        "omschrijving": "Tozo 4 Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    # Na besluit
    "794": {
        "omschrijving": "Tozo 4 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": E_AANVRAAG_STEP_ID["inkomstenwijziging"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
    },
    "1735650": {
        "omschrijving": "Tozo 4 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "1735645": {
        "omschrijving": "Tozo 4 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Tozo 4"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    # Tozo 5
    "837": {
        "omschrijving": "Tozo 5 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Aanvraag Tozo 5",
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "176167": {
        "omschrijving": "Tozo5 Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176165": {
        "omschrijving": "Tozo5 Afwijzen",
        "document_title": "Besluit afwijzing",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "176169": {
        "omschrijving": "Tozo5 Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "176168": {
        "omschrijving": "Tozo5 Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
        "about_specific": E_ABOUT_SPECIFIC_LENING,
    },
    "176164": {
        "omschrijving": "Tozo5 Hersteltermijn",
        "document_title": "Brief meer informatie",
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "176163": {
        "omschrijving": "Tozo5 Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "176166": {
        "omschrijving": "Tozo5 Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "176170": {
        "omschrijving": "Tozo5 Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176171": {
        "omschrijving": "Tozo5 Toekennen voorschot via batch",
        "document_title": "Brief betaling voorschot",
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "1725657": {
        "omschrijving": "Tozo5 Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    # Na besluit
    "1745650": {
        "omschrijving": "Tozo5 Terugvorderen na inkomstenopgave",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    "1745645": {
        "omschrijving": "Tozo5 Terugvorderen na inkomstenopgave (batch)",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "838": {
        "omschrijving": "Tozo 5 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": E_AANVRAAG_STEP_ID["inkomstenwijziging"],
        "about": E_AANVRAAG_ABOUT["Tozo 5"],
    },
    # TONK
    "802": {
        "omschrijving": "TONK aanvraag",
        "document_title": "Aanvraag TONK",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176137": {
        "omschrijving": "TONK hersteltermijn",
        "document_title": "Brief meer informatie",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176138": {
        "omschrijving": "TONK intrekken",
        "document_title": "Brief intrekking TONK aanvraag",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176149": {
        "omschrijving": "TONK toekennen",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176156": {
        "omschrijving": "TONK toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "176145": {
        "omschrijving": "TONK afwijzen",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176155": {
        "omschrijving": "TONK afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176146": {
        "omschrijving": "TONK Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
    },
    "176180": {
        "omschrijving": "TONK Ambtshalve verlenging via batch",
        "document_title": "Besluit verlenging",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["verlenging"],
    },
    "176182": {
        "omschrijving": "TONK Besluit over verlenging",
        "document_title": "Besluit over verlenging",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["mogelijkeVerlenging"],
    },
    "1726182": {
        "omschrijving": "TONK Bevestigen weigering verlenging",
        "document_title": "Brief bevestiging weigering",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["briefWeigering"],
    },
    "843": {
        "omschrijving": "Correctiemail Tonk",
        "document_title": "Mail verkeerde TONK-brief",
        "about": E_AANVRAAG_ABOUT["TONK"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["correctiemail"],
        "datePublished": "2021-07-15T00:00:00+01:00",
    },
    # BBZ
    "844": {
        "omschrijving": "Bbz aanvraag",
        "document_title": "Aanvraag Bbz",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
    },
    "176195": {
        "omschrijving": "Transitie Bbz Toekennen batch",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "175843": {
        "omschrijving": "Bbz toekenning bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
        "about_specific": E_ABOUT_SPECIFIC_LENING,
    },
    "175855": {
        "omschrijving": "Bbz verlenging beslistermijn met 13 weken",
        "document_title": "Brief verlenging beslistermijn",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["beslisTermijn"],
    },
    "176351": {
        "omschrijving": "Transitie Bbz Hersteltermijn",
        "document_title": "Brief verzoek om meer informatie",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
    },
    "176368": {
        "omschrijving": "Brief aanvraag adviesrapport",
        "document_title": "Brief aanvraag adviesrapport",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["briefAdviesRapport"],
    },
    "176350": {
        "omschrijving": "Transitie Bbz Intrekken",
        "document_title": "Brief intrekken Bbz aanvraag",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
    },
    "176353": {
        "omschrijving": "Transitie Bbz buiten behandeling stellen",
        "document_title": "Besluit buiten behandeling",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
    },
    "175884": {
        "omschrijving": "Bbz akte bedrijfskapitaal",
        "document_title": "Brief akte bedrijfskapitaal",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["briefAkteBedrijfskapitaal"],
    },
    "176196": {
        "omschrijving": "Transitie Bbz voorschot toekennen batch",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "176197": {
        "omschrijving": "Transitie Bbz voorschot toekennen handmatig",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "176198": {
        "omschrijving": "Transitie Bbz Afwijzen",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "1736198": {
        "omschrijving": "Transitie Bbz Afwijzen",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "176194": {
        "omschrijving": "Transitie Bbz Toekennen handmatig",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "176301": {
        "omschrijving": "Ioaz Toekenning voorlopige uitkering",
        "document_title": "Besluit toekenning",
        "about": E_AANVRAAG_ABOUT["IOAZ"],
        "about_parent": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenningVoorlopig"],
    },
    "176322": {
        "omschrijving": "Ioaz Aanvraag hersteltermijn",
        "document_title": "Brief verzoek om meer informatie",
        "about": E_AANVRAAG_ABOUT["IOAZ"],
        "about_parent": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
    },
    "176332": {
        "omschrijving": "Ioaz aanvraag buiten behandeling stellen",
        "document_title": "Besluit buiten behandeling",
        "about": E_AANVRAAG_ABOUT["IOAZ"],
        "about_parent": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
    },
    "1736301": {
        "omschrijving": "Ioaz Toekenning voorlopige uitkering",
        "document_title": "Besluit toekenning",
        "about": E_AANVRAAG_ABOUT["IOAZ"],
        "about_parent": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenningVoorlopig"],
    },
    "1736302": {
        "omschrijving": "Ioaz Toekenning definitieve uitkering",
        "document_title": "Besluit toekenning uitkering",
        "about": E_AANVRAAG_ABOUT["IOAZ"],
        "about_parent": E_AANVRAAG_ABOUT["Bbz"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "1736303": {
        "omschrijving": "Ioaz afwijzing uitkering",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["IOAZ"],
        "about_parent": E_AANVRAAG_ABOUT["Bbz"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "851": {
        "omschrijving": "BBZ2 Inkomsten Verklaring",
        "document_title": "Wijziging inkomsten Bbz",
        "step_id": E_AANVRAAG_STEP_ID["inkomstenwijziging"],
        "about": E_AANVRAAG_ABOUT["Bbz"],
    },
    "176363": {
        "omschrijving": "Transitie Bbz Terugvordering via batch",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "176365": {
        "omschrijving": "Transitie Bbz Terugvordering",
        "document_title": "Besluit terugvordering",
        "step_id": E_AANVRAAG_STEP_ID["terugvorderingsbesluit"],
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    # BBZ 3
    "853": {
        "omschrijving": "Aanvraag Bbz3",
        "document_title": "Bbz aanvraag",
        "step_id": E_AANVRAAG_STEP_ID["aanvraag"],
        "about": E_AANVRAAG_ABOUT["Bbz"],
    },
    "854": {
        "omschrijving": "Bbz3 Inkomsten verklaring",
        "document_title": "Wijziging inkomsten Bbz",
        "step_id": E_AANVRAAG_STEP_ID["inkomstenwijziging"],
        "about": E_AANVRAAG_ABOUT["Bbz"],
    },
    "175765": {
        "omschrijving": "Bbz Toekennen",
        "document_title": "Besluit toekenning",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "1735802": {
        "omschrijving": "Bbz Afwijzing",
        "document_title": "Besluit afwijzing",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "decision": E_AANVRAAG_DECISION_ID["afwijzing"],
    },
    "1735840": {
        "omschrijving": "Bbz Toekenning Bbz",
        "document_title": "Besluit toekenning",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
        "decision": E_AANVRAAG_DECISION_ID["toekenning"],
    },
    "175858": {
        "omschrijving": "Bbz Hersteltermijn aanvraag",
        "document_title": "Brief meer informatie",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["herstelTermijn"],
        "about_specific": E_ABOUT_SPECIFIC_UITKERING,
    },
    "175863": {
        "omschrijving": "Bbz Melding aanvraag adviesrapport",
        "document_title": "Brief aanvraag adviesrapport",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["briefAdviesRapport"],
    },
    "175861": {
        "omschrijving": "Bbz Intrekking",
        "document_title": "Brief intrekken Bbz aanvraag",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["intrekking"],
    },
    "175866": {
        "omschrijving": "Bbz Aanvraag buiten behandeling stellen",
        "document_title": "Besluit buiten behandeling",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
    },
    "1735866": {
        "omschrijving": "Bbz Aanvraag buiten behandeling stellen",
        "document_title": "Besluit buiten behandeling",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["buitenBehandeling"],
    },
    "175766": {
        "omschrijving": "Bbz Voorschot toekennen",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "175885": {
        "omschrijving": "Bbz Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["voorschot"],
    },
    "1538": {
        "omschrijving": "Bbz: informatie doorgeven",
        "document_title": "Bbz: informatie doorgeven",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["informatieOntvangen"],
    },
    "175874": {
        "omschrijving": "Mail",
        "document_title": "Mail Bbz",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["correctiemail"],
    },
    "1501": {
        "omschrijving": "Besluit definitieve berekening",
        "document_title": "Besluit definitieve berekening Bbz uitkering",
        "about": E_AANVRAAG_ABOUT["Bbz"],
        "step_id": E_AANVRAAG_STEP_ID["besluit"],
        "decision": E_AANVRAAG_DECISION_ID["beschikking"]
    },
}
