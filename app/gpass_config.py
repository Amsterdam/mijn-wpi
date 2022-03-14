import os

# GPASS
GPASS_API_TOKEN = os.getenv("GPASS_TOKEN")
GPASS_API_LOCATION = os.getenv("GPASS_API_LOCATION")
GPASS_FERNET_ENCRYPTION_KEY = os.getenv("FERNET_KEY")

STADSPAS_TRANSACTIONS_PATH = "/wpi/stadspas/transacties/"

# GPASS endpoints
GPASS_ENDPOINT_PAS = f"{GPASS_API_LOCATION}/rest/sales/v1/pas/"
GPASS_ENDPOINT_PASHOUDER = f"{GPASS_API_LOCATION}/rest/sales/v1/pashouder"
GPASS_ENDPOINT_TRANSACTIONS = f"{GPASS_API_LOCATION}/rest/transacties/v1/budget"

GPASS_ADMIN_NUMBER_GEMEENTE_CODE = "0363"
GPASS_BUDGET_ONLY_FOR_CHILDREN = (
    True  # NOTE: False if we also display budgets for adults.
)
