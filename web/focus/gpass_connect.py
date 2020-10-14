import json
from builtins import print

import requests


class GpassConnection:
    def __init__(self, api_location, bearer_token):
        self.api_location = api_location
        self.bearer_token = bearer_token

    def _get(self):
        pass

    def get_stadspashouder(self, admin_number):
        headers = {
            "Authorization": f"AppBearer {self.bearer_token},{admin_number}"
        }
        url = f"{self.api_location}/rest/sales/v1/pashouder"
        print(url)
        print(headers)

        response = requests.get(url, headers=headers)
        print(response.content)
        data = response.json()

        print(response.status_code)
        # print(response.json())

        passen = data['passen']

        print(json.dumps(passen, indent=True))

        passen = [pas for pas in passen if pas['actief'] is True]

        for pas in passen:
            # pasnummer = pas['pasnummer_volledig']
            pasnummer = pas['pasnummer']
            url = f'{self.api_location}/rest/sales/v1/pas/{pasnummer}'
            print(">>", url)
            print(">>>", headers)
            response = requests.get(url, headers=headers)
            print(response.content)
            print(response.status_code)
            print(json.dumps(response.json(), indent=True))

        return [{
            "id": "xxx123123123123",
            "pasnummer": "123123123123",
            "datumAfloop": "2020-12-12",
            "naam": "Ramses Rawjingakoli",
            "budgets": [
                {
                    "title": "KLEDING-EN-EDUCATIE",
                    "assigned": 220,
                    "balance": 130
                },
                {
                    "title": "SPORT-EN-SPEL",
                    "assigned": 220,
                    "balance": 80
                }
            ]
        },
            {
                "id": "xxx89899898",
                "pasnummer": "89899898",
                "datumAfloop": "2021-04-23",
                "naam": "Jawh Rawjingakoli",
                "budgets": [
                    {
                        "title": "SPORT-EN-SPEL",
                        "assigned": 220,
                        "balance": 80
                    }
                ]
            }
        ]
