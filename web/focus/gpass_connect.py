from pprint import pprint

import requests

from focus.crypto import encrypt

log_raw = False


class GpassConnection:
    def __init__(self, api_location, bearer_token):
        self.api_location = api_location
        self.bearer_token = bearer_token

    def _get(self, url, admin_number):
        url = f"{self.api_location}{url}"
        headers = {
            "Authorization": f"AppBearer {self.bearer_token},{admin_number}"
        }
        response = requests.get(url, headers=headers)
        if log_raw:
            print("url", url)
            pprint(response.json())
        return response

    def _format_budgets(self, budget):
        return {
            "description": budget["omschrijving"],
            "code": budget["code"],
            "assigned": budget["budget_assigned"],
            "balance": budget["budget_balance"],
        }

    def _format_pas_data(self, naam: str, pas: dict, admin_number: str):
        budgets = [self._format_budgets(b) for b in pas['budgetten']]

        encrypted_admin_pas = encrypt(admin_number, pas["pasnummer"])

        return {
            "id": pas["id"],
            "pasnummer": pas["pasnummer"],
            "datumAfloop": pas["expiry_date"],
            "naam": naam,
            "budgets": budgets,
            "url_transactions": f"/focus/stadspastransacties/{encrypted_admin_pas}"
        }

    def get_stadspassen(self, admin_number):
        url = "/rest/sales/v1/pashouder?addsubs=true"
        response = self._get(url, admin_number)
        data = response.json()
        naam = f"{data['initialen']} {data['achternaam']}"

        passen = data['passen']

        passen = [pas for pas in passen if pas['actief'] is True]
        passen_result = []

        for pas in passen:
            pasnummer = pas['pasnummer']
            url = f'/rest/sales/v1/pas/{pasnummer}?include_balance=true'
            response = self._get(url, admin_number)

            if response.status_code == 200:
                passen_result.append(self._format_pas_data(naam, response.json(), admin_number))
            else:
                # TODO: implement me
                pass

        # TODO: also include sub-passen
        return passen_result

    def _format_transaction(self, transaction):
        date = transaction['transactiedatum']  # parse and convert to date
        return {
            "id": transaction["id"],
            "title": "title",
            "amount": transaction["bedrag"],
            "date": date,
        }

    def get_transactions(self, admin_number, pas_number):
        url = f"/rest/transacties/v1/budget?pasnummer={pas_number}"
        response = self._get(url, admin_number)

        if response.status_code != 200:
            return None # TODO: implement me

        data = response.json()

        return [self._format_transaction(t)for t in data['transacties']]
