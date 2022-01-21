import sys
from pprint import pprint

import app.gpass_service
from app.utils import decrypt
from app.gpass_service import get_stadspassen, get_transactions
from app.utils import volledig_administratienummer

app.gpass_service.LOG_RAW = True

admin_number = sys.argv[1]

if (
    len(admin_number) != 14
):  # adminnumber padded to 10, 4 digit city code prefixed makes 14
    # pad
    admin_number = volledig_administratienummer(admin_number)


result = get_stadspassen(admin_number)
print("\n ---\nstadspassen:")
pprint(result)

pas_number = decrypt(result[0]["urlTransactions"].rsplit("/", 1)[1])[1]
print("Pas number", pas_number)

result = get_transactions(admin_number, pas_number)
print("\n ---\npas transactions", pas_number)
pprint(result)
