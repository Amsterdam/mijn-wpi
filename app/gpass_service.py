import logging

import requests

from app.config_new import API_REQUEST_TIMEOUT, GPASS_API_LOCATION, GPASS_API_TOKEN
from app.utils import encrypt


def send_request(path, admin_number):
    url = f"{GPASS_API_LOCATION}{path}"

    headers = {"Authorization": f"AppBearer {GPASS_API_TOKEN},{admin_number}"}
    response = requests.get(url, headers=headers, timeout=API_REQUEST_TIMEOUT)

    logging.debug(response)

    response.raise_for_status()

    return response


def format_transaction(transaction):
    date = transaction["transactiedatum"]  # parse and convert to date

    return {
        "id": transaction["id"],
        "title": transaction["budget"]["aanbieder"]["naam"],
        "amount": transaction["bedrag"],
        "date": date,
    }


def format_budget(budget, admin_number, pass_number):
    transactions_key = encrypt(budget["code"], admin_number, pass_number)
    url_transactions = f"/api/focus/stadspastransacties/{transactions_key}"

    return {
        "description": budget["omschrijving"],
        "code": budget["code"],
        "assigned": budget["budget_assigned"],
        "balance": budget["budget_balance"],
        "urlTransactions": url_transactions,
        "datumAfloop": budget["expiry_date"],
    }


def format_stadspas(naam: str, pas: dict, admin_number: str):
    budgets = [
        format_budget(budget, admin_number, pas["pasnummer"])
        for budget in pas["budgetten"]
    ]

    return {
        "id": pas["id"],
        "pasnummer": pas["pasnummer_volledig"],
        "datumAfloop": pas["expiry_date"],
        "naam": naam,
        "budgets": budgets,
    }


def format_stadspassen(stadspas_owner, admin_number):
    try:
        naam = stadspas_owner["volledige_naam"]
    except KeyError:
        # TODO: remove me when gpass prod is updated to provide volledige_naam
        try:
            naam = f'{stadspas_owner["initialen"]} {stadspas_owner["achternaam"]}'
        except KeyError as e:
            logging.error(f"{type(e)} available: {stadspas_owner.keys()}")
            raise e

    stadspassen_actief = [
        pas for pas in stadspas_owner["passen"] if pas["actief"] is True
    ]

    stadspassen = []

    for stadspas in stadspassen_actief:
        pass_number = stadspas["pasnummer"]
        path = f"/rest/sales/v1/pas/{pass_number}?include_balance=true"

        response = send_request(path, admin_number)

        stadspassen.append(format_stadspas(naam, response.json(), admin_number))

    # TODO: also include sub-passen
    return stadspassen


def get_stadspassen(admin_number):
    path = "/rest/sales/v1/pashouder?addsubs=true"
    response = send_request(path, admin_number)

    stadspas_owner = response.json()

    if not stadspas_owner:
        return []

    stadspassen = format_stadspassen(stadspas_owner, admin_number)

    if stadspas_owner["sub_pashouders"]:
        for sub_owner in stadspas_owner["sub_pashouders"]:
            # Merge lists
            stadspassen += format_stadspassen(sub_owner, admin_number)

    return stadspassen


def get_transactions(admin_number, pass_number, budget_code):
    path = f"/rest/transacties/v1/budget?pasnummer={pass_number}&budgetcode={budget_code}&sub_transactions=true"
    response = send_request(path, admin_number)

    response_json = response.json()

    if not "transacties" in response_json:
        return []

    transactions = response_json["transacties"]

    if not transactions:
        return []

    return [format_transaction(transaction) for transaction in transactions]
