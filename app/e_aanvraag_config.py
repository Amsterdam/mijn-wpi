from app.focus_config import FOCUS_STEP_ID_TRANSLATIONS


E_AANVRAAG_PRODUCT_NAMES = [
    "Tozo 1",
    "Tozo 2",
    "Tozo 3",
    "Tozo 4",
    "Tozo 5",
    "TONK",
    "bbz",
    "ioaz",
]

E_AANVRAAG_PRODUCT_TITLES = {
    "tozo 1": "Tozo 1 (aangevraagd voor 1 juni 2020)",
    "tozo 2": "Tozo 2 (aangevraagd vanaf 1 juni 2020)",
    "tozo 3": "Tozo 3 (aangevraagd vanaf 1 oktober 2020)",
    "tozo 4": "Tozo 4 (aangevraagd vanaf 1 april 2021)",
    "tozo 5": "Tozo 5 (aangevraagd vanaf 1 juli 2021)",
    "tonk": "TONK",
    "bbz": "Bbz",
    "ioaz": "Ioaz",
}

E_AANVRAAG_STEP_ID_TRANSLATIONS = {
    **FOCUS_STEP_ID_TRANSLATIONS,
    # Tozo 1-5 / Bbz
    "voorschot": "Voorschot",
    "terugvorderingsbesluit": "Terugvorderings- besluit",
    # Tozo 1-5 / Bbz
    "inkomstenwijziging": "Wijziging inkomsten",
    # Bbz
    "briefAdviesRapport": "Brief",
    "briefAkteBedrijfskapitaal": "Akte",
    "beslisTermijn": "Tijd nodig",
    # TONK
    "correctiemail": "Mail",
    "briefWeigering": "Brief",
}

E_AANVRAAG_DOCUMENT_CONFIG = {
    # Tozo 1
    "756": {
        "omschrijving": "Verkorte Aanvraag BBZ",
        "document_title": "Ontvangst- bevestiging Aanvraag",
        "product": "Tozo 1",
        "step_id": "aanvraag",
    },
    "770": {
        "omschrijving": "Tegemoetkoming Ondernemers en Zelfstandigen",
        "document_title": "Ontvangst- bevestiging Aanvraag",
        "product": "Tozo 1",
        "step_id": "aanvraag",
    },
    "175296": {
        "omschrijving": "Toekennen voorschot Tozo",
        "document_title": "Brief betaling voorschot",
        "product": "Tozo 1",
        "step_id": "voorschot",
    },
    "175299": {
        "omschrijving": "Bbz Toekennen voorschot Tozo via batch",
        "document_title": "Brief betaling voorschot",
        "product": "Tozo 1",
        "step_id": "voorschot",
    },
    "175303": {
        "omschrijving": "Tozo Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "product": "Tozo 1",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "175304": {
        "omschrijving": "Tozo Afwijzen",
        "document_title": "Besluit afwijzing",
        "product": "Tozo 1",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    "175305": {
        "omschrijving": "Tozo Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "product": "Tozo 1",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
    },
    "175306": {
        "omschrijving": "Tozo Hersteltermijn",
        "document_title": "Brief meer informatie",
        "product": "Tozo 1",
        "step_id": "herstelTermijn",
    },
    "175308": {
        "omschrijving": "Tozo Terugvordering voorschot",
        "document_title": "Besluit afwijzing",
        "product": "Tozo 1",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    "175311": {
        "omschrijving": "Tozo Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "product": "Tozo 1",
        "product_specific": "lening",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "175314": {
        "omschrijving": "Tozo Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "product": "Tozo 1",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "175317": {
        "omschrijving": "Tozo Intrekken met terugvordering voorschot",
        "document_title": "Besluit intrekking met terugbetaling",
        "product": "Tozo 1",
        "step_id": "besluit",
        "decision": "intrekking",
    },
    "175331": {
        "omschrijving": "Tozo Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "product": "Tozo 1",
        "step_id": "besluit",
        "decision": "intrekking",
    },
    "175334": {
        "omschrijving": "Tozo Vrije beschikking",
        "document_title": "Besluit Tozo 1 aanvraag",
        "product": "Tozo 1",
        "step_id": "besluit",
        "decision": "vrijeBeschikking",
    },
    "175335": {
        "omschrijving": "Tozo Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "product": "Tozo 1",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    # TOZO 2
    "777": {
        "omschrijving": "TOZO 2 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Ontvangst- bevestiging Aanvraag",
        "product": "Tozo 2",
        "step_id": "aanvraag",
    },
    "175336": {
        "omschrijving": "Tozo2 Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "product": "Tozo 2",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "175337": {
        "omschrijving": "Tozo2 Afwijzen",
        "document_title": "Besluit afwijzing",
        "product": "Tozo 2",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    "175338": {
        "omschrijving": "Tozo2 Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "product": "Tozo 2",
        "product_specific": "lening",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "175340": {
        "omschrijving": "Tozo2 Hersteltermijn",
        "document_title": "Brief meer informatie",
        "product": "Tozo 2",
        "step_id": "herstelTermijn",
    },
    "175341": {
        "omschrijving": "Tozo2 Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "product": "Tozo 2",
        "step_id": "besluit",
        "decision": "intrekking",
    },
    "175342": {
        "omschrijving": "Tozo2 Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "product": "Tozo 2",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
    },
    "175343": {
        "omschrijving": "Tozo2 Terugvordering voorschot",
        "document_title": "Besluit terugvordering",
        "product": "Tozo 2",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    "175344": {
        "omschrijving": "Tozo2 Intrekken met terugvordering voorschot",
        "document_title": "Besluit intrekking met terugbetaling",
        "product": "Tozo 2",
        "step_id": "besluit",
        "decision": "intrekking",
    },
    "175345": {
        "omschrijving": "Tozo2 Toekennen voorschot via batch",
        "document_title": "Brief betaling voorschot",
        "product": "Tozo 2",
        "step_id": "voorschot",
    },
    "175346": {
        "omschrijving": "Tozo2 Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "product": "Tozo 2",
        "step_id": "voorschot",
    },
    "175347": {
        "omschrijving": "Tozo2 Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "product": "Tozo 2",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "175359": {
        "omschrijving": "Tozo2 Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "product": "Tozo 2",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    # Na besluit
    "790": {
        "omschrijving": "Tozo 2 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": "inkomstenwijziging",
        "product": "Tozo 2",
    },
    "175650": {
        "omschrijving": "Tozo 2 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Tozo 2",
        "product_specific": "uitkering",
    },
    "175645": {
        "omschrijving": "Tozo 2 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Tozo 2",
        "product_specific": "uitkering",
    },
    # TOZO 3
    "785": {
        "omschrijving": "TOZO 3 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Ontvangst- bevestiging Aanvraag",
        "product": "Tozo 3",
        "step_id": "aanvraag",
    },
    "175309": {
        "omschrijving": "Tozo3 Toekennen",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 3",
        "product_specific": "uitkering",
        "document_title": "Besluit toekenning uitkering",
    },
    "175307": {
        "omschrijving": "Tozo3 Toekennen voorschot",
        "step_id": "voorschot",
        "product": "Tozo 3",
        "document_title": "Brief betaling voorschot",
    },
    "175310": {
        "omschrijving": "Tozo3 Hersteltermijn",
        "step_id": "herstelTermijn",
        "product": "Tozo 3",
        "document_title": "Brief meer informatie",
    },
    "175357": {
        "omschrijving": "Tozo3 Toekennen via batch",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 3",
        "product_specific": "uitkering",
        "document_title": "Besluit toekenning uitkering",
    },
    "175358": {
        "omschrijving": "Tozo3 Buiten behandeling laten",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
        "product": "Tozo 3",
        "document_title": "Besluit buiten behandeling",
    },
    "175364": {
        "omschrijving": "Tozo3 Afwijzen",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product": "Tozo 3",
        "document_title": "Besluit afwijzing",
    },
    "175367": {
        "omschrijving": "Tozo3 Intrekken met terugvordering voorschot",
        "step_id": "besluit",
        "decision": "intrekking",
        "product": "Tozo 3",
        "document_title": "Besluit intrekking met terugbetaling",
    },
    "175368": {
        "omschrijving": "Tozo3 Terugvordering voorschot",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product": "Tozo 3",
        "document_title": "Besluit terugvordering",
    },
    "175369": {
        "omschrijving": "Tozo3 Toekennen bedrijfskapitaal",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 3",
        "product_specific": "lening",
        "document_title": "Besluit toekenning lening",
    },
    "175370": {
        "omschrijving": "Tozo3 Intrekken",
        "step_id": "besluit",
        "decision": "intrekking",
        "product": "Tozo 3",
        "document_title": "Brief intrekking aanvraag",
    },
    "175371": {
        "omschrijving": "Tozo3 Afwijzen via batch",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product": "Tozo 3",
        "document_title": "Besluit afwijzing",
    },
    "175372": {
        "omschrijving": "Tozo3 Toekennen voorschot via batch",
        "step_id": "voorschot",
        "product": "Tozo 3",
        "document_title": "Brief betaling voorschot",
    },
    # Na besluit
    "792": {
        "omschrijving": "Tozo 3 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": "inkomstenwijziging",
        "product": "Tozo 3",
    },
    "1725650": {
        "omschrijving": "Tozo 3 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Tozo 3",
        "product_specific": "uitkering",
    },
    "1725645": {
        "omschrijving": "Tozo 3 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Tozo 3",
        "product_specific": "uitkering",
    },
    # TOZO 4
    "800": {
        "omschrijving": "Tozo 4 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Ontvangst- bevestiging Aanvraag",
        "step_id": "aanvraag",
        "product": "Tozo 4",
    },
    "175654": {
        "omschrijving": "Tozo 4 Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 4",
        "product_specific": "uitkering",
    },
    "175651": {
        "omschrijving": "Tozo 4 Afwijzen",
        "document_title": "Besluit afwijzing",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product": "Tozo 4",
    },
    "175673": {
        "omschrijving": "Tozo 4 Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product": "Tozo 4",
    },
    "175656": {
        "omschrijving": "Tozo 4 Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 4",
        "product_specific": "lening",
    },
    "175689": {
        "omschrijving": "Tozo 4 Hersteltermijn",
        "document_title": "Brief meer informatie",
        "step_id": "herstelTermijn",
        "product": "Tozo 4",
    },
    "175670": {
        "omschrijving": "Tozo 4 Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "step_id": "besluit",
        "decision": "intrekking",
        "product": "Tozo 4",
    },
    "175652": {
        "omschrijving": "Tozo 4 Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
        "product": "Tozo 4",
    },
    "175677": {
        "omschrijving": "Tozo 4 Toekennen voorschot via batch",
        "document_title": "Brief betaling voorschot",
        "step_id": "voorschot",
        "product": "Tozo 4",
    },
    "175657": {
        "omschrijving": "Tozo 4 Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "step_id": "voorschot",
        "product": "Tozo 4",
    },
    "175674": {
        "omschrijving": "Tozo 4 Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 4",
        "product_specific": "uitkering",
    },
    # Na besluit
    "794": {
        "omschrijving": "Tozo 4 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": "inkomstenwijziging",
        "product": "Tozo 4",
    },
    "1735650": {
        "omschrijving": "Tozo 4 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Tozo 4",
        "product_specific": "uitkering",
    },
    "1735645": {
        "omschrijving": "Tozo 4 Terugvorderingsbesluit",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Tozo 4",
        "product_specific": "uitkering",
    },
    # Tozo 5
    "837": {
        "omschrijving": "Tozo 5 (vervolgregeling tegemoetkoming Ondernemers en Zelfstandigen)",
        "document_title": "Ontvangst- bevestiging Aanvraag",
        "step_id": "aanvraag",
        "product": "Tozo 5",
    },
    "176167": {
        "omschrijving": "Tozo5 Toekennen",
        "document_title": "Besluit toekenning uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 5",
        "product_specific": "uitkering",
    },
    "176165": {
        "omschrijving": "Tozo5 Afwijzen",
        "document_title": "Besluit afwijzing",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product": "Tozo 5",
    },
    "176169": {
        "omschrijving": "Tozo5 Afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product": "Tozo 5",
    },
    "176168": {
        "omschrijving": "Tozo5 Toekennen bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 5",
        "product_specific": "lening",
    },
    "176164": {
        "omschrijving": "Tozo5 Hersteltermijn",
        "document_title": "Brief meer informatie",
        "step_id": "herstelTermijn",
        "product": "Tozo 5",
    },
    "176163": {
        "omschrijving": "Tozo5 Intrekken",
        "document_title": "Brief intrekking aanvraag",
        "step_id": "besluit",
        "decision": "intrekking",
        "product": "Tozo 5",
    },
    "176166": {
        "omschrijving": "Tozo5 Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
        "product": "Tozo 5",
    },
    "176170": {
        "omschrijving": "Tozo5 Toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
        "product": "Tozo 5",
        "product_specific": "uitkering",
    },
    "176171": {
        "omschrijving": "Tozo5 Toekennen voorschot via batch",
        "document_title": "Brief betaling voorschot",
        "step_id": "voorschot",
        "product": "Tozo 5",
    },
    "1725657": {
        "omschrijving": "Tozo5 Toekennen voorschot",
        "document_title": "Brief betaling voorschot",
        "step_id": "voorschot",
        "product": "Tozo 5",
    },
    # Na besluit
    "1745650": {
        "omschrijving": "Tozo5 Terugvorderen na inkomstenopgave",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product_specific": "uitkering",
        "product": "Tozo 5",
    },
    "1745645": {
        "omschrijving": "Tozo5 Terugvorderen na inkomstenopgave (batch)",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Tozo 5",
        "product_specific": "uitkering",
    },
    "838": {
        "omschrijving": "Tozo 5 inkomstenwijziging",
        "document_title": "Wijziging inkomsten",
        "step_id": "inkomstenwijziging",
        "product": "Tozo 5",
    },
    # TONK
    "802": {
        "omschrijving": "TONK aanvraag",
        "document_title": "Aanvraag TONK",
        "product": "TONK",
        "step_id": "aanvraag",
        "product_specific": "uitkering",
    },
    "176137": {
        "omschrijving": "TONK hersteltermijn",
        "document_title": "Brief meer informatie",
        "product": "TONK",
        "step_id": "herstelTermijn",
        "product_specific": "uitkering",
    },
    "176138": {
        "omschrijving": "TONK intrekken",
        "document_title": "Brief intrekking TONK aanvraag",
        "product": "TONK",
        "step_id": "besluit",
        "decision": "intrekking",
        "product_specific": "uitkering",
    },
    "176149": {
        "omschrijving": "TONK toekennen",
        "document_title": "Besluit toekenning uitkering",
        "product": "TONK",
        "step_id": "besluit",
        "decision": "toekenning",
        "product_specific": "uitkering",
    },
    "176156": {
        "omschrijving": "TONK toekennen via batch",
        "document_title": "Besluit toekenning uitkering",
        "product": "TONK",
        "step_id": "besluit",
        "product_specific": "uitkering",
        "decision": "toekenning",
    },
    "176145": {
        "omschrijving": "TONK afwijzen",
        "document_title": "Besluit afwijzing",
        "product": "TONK",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product_specific": "uitkering",
    },
    "176155": {
        "omschrijving": "TONK afwijzen via batch",
        "document_title": "Besluit afwijzing",
        "product": "TONK",
        "step_id": "besluit",
        "decision": "afwijzing",
        "product_specific": "uitkering",
    },
    "176146": {
        "omschrijving": "TONK Buiten behandeling laten",
        "document_title": "Besluit buiten behandeling",
        "product": "TONK",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
    },
    "176180": {
        "omschrijving": "TONK Ambtshalve verlenging via batch",
        "document_title": "Besluit verlenging",
        "product": "TONK",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "verlenging",
    },
    "176182": {
        "omschrijving": "TONK Besluit over verlenging",
        "document_title": "Besluit over verlenging",
        "product": "TONK",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "verlenging",
    },
    "1726182": {
        "omschrijving": "TONK Bevestigen weigering verlenging",
        "document_title": "Brief bevestiging weigering",
        "product": "TONK",
        "product_specific": "uitkering",
        "step_id": "briefWeigering",
    },
    "843": {
        "omschrijving": "Correctiemail Tonk",
        "document_title": "Mail verkeerde TONK-brief",
        "product": "TONK",
        "product_specific": "uitkering",
        "step_id": "correctiemail",
        "datePublished": "2021-07-15T00:00:00+01:00",
    },
    # BBZ
    "844": {
        "omschrijving": "Bbz aanvraag",
        "document_title": "Aanvraag Bbz",
        "product": "Bbz",
        "step_id": "aanvraag",
    },
    "176195": {
        "omschrijving": "Transitie Bbz Toekennen batch",
        "document_title": "Besluit toekenning uitkering",
        "product": "Bbz",
        "step_id": "besluit",
        "decision": "toekenning",
        "product_specific": "uitkering",
    },
    "175843": {
        "omschrijving": "Bbz toekenning bedrijfskapitaal",
        "document_title": "Besluit toekenning lening",
        "product": "Bbz",
        "step_id": "besluit",
        "decision": "toekenning",
        "product_specific": "lening",
    },
    "175855": {
        "omschrijving": "Bbz verlenging beslistermijn met 13 weken",
        "document_title": "Brief verlenging beslistermijn",
        "product": "Bbz",
        "step_id": "beslisTermijn",
    },
    "176351": {
        "omschrijving": "Transitie Bbz Hersteltermijn",
        "document_title": "Brief verzoek om meer informatie",
        "product": "Bbz",
        "step_id": "herstelTermijn",
    },
    "176368": {
        "omschrijving": "Brief aanvraag adviesrapport",
        "document_title": "Brief aanvraag adviesrapport",
        "product": "Bbz",
        "step_id": "briefAdviesRapport",
    },
    "176350": {
        "omschrijving": "Transitie Bbz Intrekken",
        "document_title": "Brief intrekken Bbz aanvraag",
        "product": "Bbz",
        "step_id": "besluit",
        "decision": "intrekking",
    },
    "176353": {
        "omschrijving": "Transitie Bbz buiten behandeling stellen",
        "document_title": "Besluit buiten behandeling",
        "product": "Bbz",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
    },
    "175884": {
        "omschrijving": "Bbz akte bedrijfskapitaal",
        "document_title": "Brief akte bedrijfskapitaal",
        "product": "Bbz",
        "step_id": "briefAkteBedrijfskapitaal",
    },
    "176196": {
        "omschrijving": "Transitie Bbz voorschot toekennen batch",
        "document_title": "Brief betaling voorschot",
        "product": "Bbz",
        "step_id": "voorschot",
    },
    "176197": {
        "omschrijving": "Transitie Bbz voorschot toekennen handmatig",
        "document_title": "Brief betaling voorschot",
        "product": "Bbz",
        "step_id": "voorschot",
    },
    "176198": {
        "omschrijving": "Transitie Bbz Afwijzen",
        "document_title": "Besluit afwijzing",
        "product": "Bbz",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    "176194": {
        "omschrijving": "Transitie Bbz Toekennen handmatig",
        "document_title": "Besluit toekenning uitkering",
        "product": "Bbz",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "176301": {
        "omschrijving": "Ioaz Toekenning voorlopige uitkering",
        "document_title": "Besluit toekenning",
        "product": "IOAZ",
        "step_id": "besluit",
        "decision": "toekenningVoorlopig",
    },
    "176322": {
        "omschrijving": "Ioaz Aanvraag hersteltermijn",
        "document_title": "Brief verzoek om meer informatie",
        "product": "IOAZ",
        "step_id": "herstelTermijn",
    },
    "176332": {
        "omschrijving": "Ioaz aanvraag buiten behandeling stellen",
        "document_title": "Besluit buiten behandeling",
        "product": "IOAZ",
        "step_id": "besluit",
        "decision": "buitenBehandeling",
    },
    "1736301": {
        "omschrijving": "Ioaz Toekenning voorlopige uitkering",
        "document_title": "Besluit toekenning",
        "product": "IOAZ",
        "step_id": "besluit",
        "decision": "toekenningVoorlopig",
    },
    "1736302": {
        "omschrijving": "Ioaz Toekenning definitieve uitkering",
        "document_title": "Besluit toekenning uitkering",
        "product": "IOAZ",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "toekenning",
    },
    "1736303": {
        "omschrijving": "Ioaz afwijzing uitkering",
        "document_title": "Besluit afwijzing",
        "product": "IOAZ",
        "product_specific": "uitkering",
        "step_id": "besluit",
        "decision": "afwijzing",
    },
    "851": {
        "omschrijving": "BBZ2 Inkomsten Verklaring",
        "document_title": "Wijziging inkomsten Bbz",
        "step_id": "inkomstenwijziging",
        "product": "Bbz",
    },
    "176363": {
        "omschrijving": "Transitie Bbz Terugvordering via batch",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Bbz",
        "product_specific": "uitkering",
    },
    "176364": {
        "omschrijving": "Transitie Bbz Terugvordering",
        "document_title": "Besluit terugvordering",
        "step_id": "besluit",
        "decision": "terugvordering",
        "product": "Bbz",
        "product_specific": "uitkering",
    },
}
