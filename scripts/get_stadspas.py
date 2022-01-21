import sys
from pprint import pprint

from app.gpass_service import get_transactions
from app.config import focus_credentials, zeep_config
from app.focusconnect import FocusConnection
from app.focusserver import FocusServer
from app.utils import decrypt
from tests.test_gpass import GpassServiceTest

bsn = sys.argv[1]

focus_connection = FocusConnection(zeep_config, focus_credentials)
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

    transactions = get_transactions(admin_number, stadspas_number, budget_code)
    print("=== transactions result:")
    pprint(transactions)
