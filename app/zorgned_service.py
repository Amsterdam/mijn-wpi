import json
import logging
import requests
from dpath import util as dpath_util

from app.config import (
    SERVER_CLIENT_CERT,
    SERVER_CLIENT_KEY,
    ZORGNED_API_REQUEST_TIMEOUT_SECONDS,
    ZORGNED_API_TOKEN,
    ZORGNED_API_URL,
    ZORGNED_GEMEENTE_CODE,
    BESCHIKT_PRODUCT_RESULTAAT,
    ARMOEDE_REGELING_PRODUCT_CODES
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


def date_in_past(date):
    return (
        date
        and to_date(date) <= date.today()
    )


def filter_aanvragen(aanvragen_source=[]):
    aanvragen = []

    for aanvraag_source in aanvragen_source:
        beschikking = dpath_util.get(aanvraag_source, "beschikking", default=None)
        beschikte_producten = dpath_util.get(
            beschikking, "beschikteProducten", default=None
        )

        if beschikte_producten:
            for beschikt_product in beschikte_producten:
                product = beschikt_product.get("product")
                toegewezen_product = beschikt_product.get("toegewezenProduct")
                # Only select products which match these criteria
                if beschikt_product.get("resultaat") in BESCHIKT_PRODUCT_RESULTAAT and product.get("productsoortCode") in ARMOEDE_REGELING_PRODUCT_CODES and date_in_past(toegewezen_product.get("datumIngangGeldigheid")):
                    aanvragen.append(aanvraag_source)

    return aanvragen


def get_armoede_aanvragen(bsn, query_params=None):
    response_data = send_api_request_json(
        bsn,
        "/aanvragen",
        query_params,
    )
    response_aanvragen = response_data["_embedded"]["aanvraag"]

    return filter_aanvragen(response_aanvragen)


def get_clientnummer(bsn):
    if(len(get_armoede_aanvragen(bsn)) == 0):
        return None

    response_data = send_api_request_json(
        bsn,
        "/persoonsgegevensNAW",
    )

    return response_data["persoon"]["clientidentificatie"]