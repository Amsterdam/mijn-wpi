import sys
from pprint import pprint

import app.focusconnect
import app.gpass_service
from app import config_new, credentials
from app.focusconnect import FocusConnection
from app.focusserver import FocusServer
from app.utils import decrypt

bsn = sys.argv[1]

focus_connection = FocusConnection(config_new, credentials)
# Serve the FOCUS requests that are exposed by this server
focus_server = FocusServer(focus_connection)

stadspas = focus_server._collect_stadspas_data(bsn)

print("=== stadspas result:")
pprint(stadspas)

if stadspas["stadspassen"]:
    transactions_url = stadspas["stadspassen"][0]["budgets"][0]["urlTransactions"]
    budget_code, admin_number, stadspas_number = decrypt(
        transactions_url.rsplit("/", 1)[1]
    )

    transactions = app.gpass_service.get_transactions(
        admin_number, stadspas_number, budget_code
    )
    print("=== transactions result:")
    pprint(transactions)
