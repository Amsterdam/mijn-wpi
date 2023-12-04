import json
import logging
import requests
from app.config import (
    SERVER_CLIENT_CERT,
    SERVER_CLIENT_KEY,
    ZORGNED_API_REQUEST_TIMEOUT_SECONDS,
    ZORGNED_API_TOKEN,
    ZORGNED_API_URL,
    ZORGNED_GEMEENTE_CODE,
)


def send_api_request(bsn, operation="", post_message={}):
    headers = None
    cert = None

    headers = {"Token": ZORGNED_API_TOKEN}
    cert = (SERVER_CLIENT_CERT, SERVER_CLIENT_KEY)

    url = f"{ZORGNED_API_URL}{operation}"
    default_post_params = {
        "burgerservicenummer": bsn,
        "gemeentecode": ZORGNED_GEMEENTE_CODE,
    }

    res = requests.post(
        url,
        timeout=ZORGNED_API_REQUEST_TIMEOUT_SECONDS,
        headers=headers,
        cert=cert,
        json=default_post_params | post_message  # Pipe operator merges the 2 dicts
    )

    return res


def send_api_request_json(bsn, operation="", post_message={}):
    res = send_api_request(bsn, operation, post_message)

    # 404 means bsn is now known to ZorgNed
    if len(res.content) < 1 or res.status_code == 404:
        return None

    # Other error codes should be propagated
    res.raise_for_status()

    response_data = res.json()

    logging.debug(json.dumps(response_data, indent=4))

    return response_data


def get_clientnummer(bsn):
    response_data = send_api_request_json(
        bsn,
        "/persoonsgegevensNAW",
    )

    if (
        response_data is not None
        and "persoon" in response_data
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
