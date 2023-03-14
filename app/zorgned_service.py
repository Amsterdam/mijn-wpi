import json
import logging
from datetime import date

import requests
from dpath import util as dpath_util

from app.config import (
    ARMOEDE_REGELING_PRODUCT_CODES,
    BESCHIKT_PRODUCT_RESULTAAT,
    SERVER_CLIENT_CERT,
    SERVER_CLIENT_KEY,
    ZORGNED_API_REQUEST_TIMEOUT_SECONDS,
    ZORGNED_API_TOKEN,
    ZORGNED_API_URL,
    ZORGNED_GEMEENTE_CODE,
)
from app.utils import to_date


def send_api_request(bsn, operation="", query_params=None):
    headers = None
    cert = None

    headers = {"Token": ZORGNED_API_TOKEN}
    cert = (SERVER_CLIENT_CERT, SERVER_CLIENT_KEY)
    url = f"{ZORGNED_API_URL}/gemeenten/{ZORGNED_GEMEENTE_CODE}/ingeschrevenpersonen/{bsn}{operation}"

    res = requests.get(
        url,
        timeout=ZORGNED_API_REQUEST_TIMEOUT_SECONDS,
        headers=headers,
        cert=cert,
        params=query_params,
    )

    res.raise_for_status()

    return res


def send_api_request_json(bsn, operation="", query_params=None):
    res = send_api_request(bsn, operation, query_params)

    response_data = res.json()

    logging.debug(json.dumps(response_data, indent=4))

    return response_data


def date_in_past(past_date):
    return past_date and to_date(past_date) <= date.today()


def has_armoede_producten(aanvragen_source=[]):
    for aanvraag_source in aanvragen_source:
        beschikking = dpath_util.get(aanvraag_source, "beschikking", default=None)
        beschikte_producten = dpath_util.get(
            beschikking, "beschikteProducten", default=None
        )

        if beschikte_producten:
            for beschikt_product in beschikte_producten:
                product = beschikt_product.get("product")
                # If any one product matches out criteria return True
                if (
                    beschikt_product.get("resultaat") in BESCHIKT_PRODUCT_RESULTAAT
                    and product.get("identificatie")
                    in ARMOEDE_REGELING_PRODUCT_CODES
                ):
                    return True

    return False


def get_aanvragen(bsn, query_params=None):
    response_data = send_api_request_json(
        bsn,
        "/aanvragen",
        query_params,
    )
    response_aanvragen = response_data["_embedded"]["aanvraag"]

    return response_aanvragen


def get_clientnummer(bsn):
    armoede_aanvragen = get_aanvragen(bsn)
    if not has_armoede_producten(armoede_aanvragen):
        return None

    response_data = send_api_request_json(
        bsn,
        "/persoonsgegevensNAW",
    )

    return response_data["persoon"]["clientidentificatie"]
