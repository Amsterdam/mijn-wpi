import logging
import json
import requests

from app.config import API_REQUEST_TIMEOUT
from app.gpass_config import (
    GPASS_API_TOKEN,
    GPASS_BUDGET_ONLY_FOR_CHILDREN,
    GPASS_ENDPOINT_PASHOUDER,
    GPASS_ENDPOINT_PAS,
    GPASS_ENDPOINT_TRANSACTIONS,
    STADSPAS_TRANSACTIONS_PATH,
)
from app.utils import encrypt
from sentry_sdk import capture_message


def send_request(url, admin_number, params=None):
    headers = {"Authorization": f"AppBearer {GPASS_API_TOKEN},{admin_number}"}
    response = requests.get(
        url, headers=headers, timeout=API_REQUEST_TIMEOUT, params=params
    )

    logging.debug(response)

    if response.status_code in [401, 404]:
        # unknown user results in a invalid token?
        logging.error(f"Gpass request error: {response.status_code}, {response.text}")
        return None

    response.raise_for_status()

    return response.json()


def format_budget(budget, admin):
    transactions_key = encrypt(
        budget["code"], admin["admin_number"], admin["pass_number"]
    )
    url_transactions = f"{STADSPAS_TRANSACTIONS_PATH + transactions_key}"

    return {
        "description": budget["omschrijving"],
        "code": budget["code"],
        "budgetAssigned": budget["budget_assigned"],
        "budgetBalance": budget["budget_balance"],
        "urlTransactions": url_transactions,
        "dateEnd": budget["expiry_date"],
    }


def format_stadspas(stadspas, admin):
    budgets = [format_budget(budget, admin) for budget in stadspas["budgetten"]]

    return {
        "id": str(stadspas["id"]),
        "owner": admin["owner"],
        "dateEnd": stadspas["expiry_date"],
        "budgets": budgets,
        "passNumber": stadspas["pasnummer_volledig"],
        "passType": "kind" if budgets and GPASS_BUDGET_ONLY_FOR_CHILDREN else "ouder",
    }


def get_stadspas_details(admin):
    stadspas_number = admin["pass_number"]
    admin_number = admin["admin_number"]

    path = f"{GPASS_ENDPOINT_PAS}{stadspas_number}"

    stadspas = send_request(path, admin_number, params={"include_balance": True})

    if not stadspas:
        return None

    stadspas_details = format_stadspas(stadspas, admin)

    return stadspas_details


def get_admins(admin_number, owner_name, stadspassen, category_filter=None):
    stadspassen_active = [pas for pas in stadspassen if pas["categorie_code"] == category_filter] if category_filter is not None else stadspassen
    stadspassen = []

    for stadspas in stadspassen_active:
        stadspas_details = {
            "owner": owner_name,
            "pass_number": str(stadspas["pasnummer"]),
            "admin_number": admin_number,
        }
        stadspassen.append(stadspas_details)

    return stadspassen


def get_owner_name(stadspas_owner):
    name = stadspas_owner.get("volledige_naam")

    if not name:
        name = f'{stadspas_owner["initialen"]} {stadspas_owner["achternaam"]}'

    return name


def get_stadspas_admins(admin_number, category_filter):
    stadspas_owner = send_request(
        GPASS_ENDPOINT_PASHOUDER, admin_number, params={"addsubs": True}
    )

    if not stadspas_owner:
        return []

    capture_message(json.dumps(stadspas_owner["passen"]))

    owner_name = get_owner_name(stadspas_owner)
    stadspas_admins = get_admins(admin_number, owner_name, stadspas_owner["passen"], category_filter)

    if stadspas_owner["sub_pashouders"]:
        for sub_stadspas_owner in stadspas_owner["sub_pashouders"]:
            owner_name = get_owner_name(sub_stadspas_owner)
            stadspas_admins += get_admins(
                admin_number, owner_name, sub_stadspas_owner["passen"]
            )

    return stadspas_admins


def get_stadspassen(admin_number, category_filter=None):
    stadspas_admins = get_stadspas_admins(admin_number, category_filter)
    stadspassen = []

    for admin in stadspas_admins:
        stadspas_details = get_stadspas_details(admin)

        if stadspas_details:
            stadspassen.append(stadspas_details)

    return stadspassen


def format_transaction(transaction):
    date_published = transaction["transactiedatum"]  # parse and convert to date

    return {
        "id": str(transaction["id"]),
        "title": transaction["budget"]["aanbieder"]["naam"],
        "amount": transaction["bedrag"],
        "datePublished": date_published,
    }


def get_transactions(admin_number, pass_number, budget_code):
    params = {
        "pasnummer": pass_number,
        "budgetcode": budget_code,
        "sub_transactions": True,
    }
    response = send_request(GPASS_ENDPOINT_TRANSACTIONS, admin_number, params=params)

    if not response:
        return []

    transactions = response.get("transacties")

    if not transactions:
        return []

    return [format_transaction(transaction) for transaction in transactions]
