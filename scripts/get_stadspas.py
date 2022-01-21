import sys
from pprint import pprint

import app.focusconnect
import app.gpass_service
from app.config import (
    config,
    credentials,
    get_TMA_certificate,
)
from app.crypto import decrypt
from app.focusconnect import FocusConnection
from app.focusserver import FocusServer

bsn = sys.argv[1]

app.focusconnect.LOG_RAW = True
app.gpass_service.LOG_RAW = True

focus_connection = FocusConnection(config, credentials)
# Serve the FOCUS requests that are exposed by this server
focus_server = FocusServer(focus_connection, get_TMA_certificate())

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
