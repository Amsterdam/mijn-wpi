import sys
from pprint import pprint

from focus.config import get_gpass_api_location, get_gpass_bearer_token
from focus.gpass_connect import GpassConnection

from focus.crypto import decrypt

import focus.gpass_connect

from focus.utils import volledig_administratienummer

focus.gpass_connect.LOG_RAW = True

admin_number = sys.argv[1]

if len(admin_number) != 14:  # adminnumber padded to 10, 4 digit city code prefixed makes 14
    # pad
    admin_number = volledig_administratienummer(admin_number)


con = GpassConnection(get_gpass_api_location(), get_gpass_bearer_token())

result = con.get_stadspassen(admin_number)
print("\n ---\nstadspassen:")
pprint(result)

pas_number = decrypt(result[0]['urlTransactions'].rsplit('/', 1)[1])[1]
print("Pas number", pas_number)

result = con.get_transactions(admin_number, pas_number)
print("\n ---\npas transactions", pas_number)
pprint(result)
