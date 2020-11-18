from pprint import pprint

import requests

from focus.crypto import encrypt

LOG_RAW = False


class GpassConnection:
    def __init__(self, api_location, bearer_token):
        self.api_location = api_location
        self.bearer_token = bearer_token

    def _get(self, path, admin_number):
        path = f"{self.api_location}{path}"
        headers = {
            "Authorization": f"AppBearer {self.bearer_token},{admin_number}"
        }
        response = requests.get(path, headers=headers)
        if LOG_RAW:
            print("url", path, "adminnumber", admin_number, self.bearer_token)
            print("status", response.status_code)
            pprint(response.json())
        return response

    def _format_budgets(self, budget, admin_number, pas_number):
        encrypted_admin_pas = encrypt(budget['code'], admin_number, pas_number)

        return {
            "description": budget["omschrijving"],
            "code": budget["code"],
            "assigned": budget["budget_assigned"],
            "balance": budget["budget_balance"],
            "urlTransactions": f"/api/focus/stadspastransacties/{encrypted_admin_pas}"
        }

    def _format_pas_data(self, naam: str, pas: dict, admin_number: str):
        budgets = [self._format_budgets(b, admin_number, pas["pasnummer"]) for b in pas['budgetten']]

        return {
            "id": pas["id"],
            "pasnummer": pas["pasnummer_volledig"],
            "datumAfloop": pas["expiry_date"],
            "naam": naam,
            "budgets": budgets,
        }

    def get_stadspassen(self, admin_number):
        path = "/rest/sales/v1/pashouder?addsubs=true"
        response = self._get(path, admin_number)
        if response.status_code != 200:
            print("status code", response.status_code)
            # unknown user results in a invalid token?
            return []
        data = response.json()

        passes = self._format_pasholder(data, admin_number)
        for sub_holder in data['sub_pashouders']:
            passes += self._format_pasholder(sub_holder, admin_number)

        return passes

    def _format_pasholder(self, pas_holder, admin_number):
        naam = f"{pas_holder['initialen']} {pas_holder['achternaam']}"
        passen = pas_holder['passen']

        passen = [pas for pas in passen if pas['actief'] is True]
        passen_result = []

        for pas in passen:
            pasnummer = pas['pasnummer']
            path = f'/rest/sales/v1/pas/{pasnummer}?include_balance=true'
            response = self._get(path, admin_number)

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
            "title": transaction['budget']['aanbieder']['naam'],
            "amount": transaction["bedrag"],
            "date": date,
        }

    def get_transactions(self, admin_number, pas_number, budget_code):
        path = f"/rest/transacties/v1/budget?pasnummer={pas_number}&budgetcode={budget_code}&sub_transactions=true"
        response = self._get(path, admin_number)

        if response.status_code != 200:
            return None

        data = response.json()

        return [self._format_transaction(t)for t in data['transacties']]
