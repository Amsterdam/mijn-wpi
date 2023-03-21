import json
import logging
from datetime import date

import requests
from dpath import util as dpath_util

from app.config import (
    SERVER_CLIENT_CERT,
    SERVER_CLIENT_KEY,
    ZORGNED_API_REQUEST_TIMEOUT_SECONDS,
    ZORGNED_API_TOKEN,
    ZORGNED_API_URL,
    ZORGNED_GEMEENTE_CODE,
)
from app.utils import to_date
from sentry_sdk import capture_message


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

    capture_message(f"Length of response for operation {operation} {len(res)}")

    response_data = res.json()

    logging.debug(json.dumps(response_data, indent=4))

    return response_data


def get_clientnummer(bsn):
    response_data = send_api_request_json(
        bsn,
        "/persoonsgegevensNAW",
    )

    if (
        "persoon" in response_data
        and response_data["persoon"]
        and "clientidentificatie" in response_data["persoon"]
        and response_data["persoon"]["clientidentificatie"]
    ):
        return response_data["persoon"]["clientidentificatie"]

    return None


def volledig_clientnummer(identificatie) -> str:
    clientnummer = str(identificatie).zfill(10)
    clientnummer = f"{ZORGNED_GEMEENTE_CODE}{clientnummer}"
    return clientnummer
