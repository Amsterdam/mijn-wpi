from cryptography.fernet import Fernet

from app.config_new import GPASS_FERNET_ENCRYPTION_KEY


def volledig_administratienummer(admin_number) -> str:
    """
    Return the complete admin number used in gpass

    Pad to 10 chars and add a static "gemeente code"
    """
    stadspas_admin_number = str(admin_number).zfill(10)
    stadspas_admin_number = f"0363{stadspas_admin_number}"
    return stadspas_admin_number


def encrypt(budget_code: str, admin_number: str, pas_number) -> str:
    f = Fernet(GPASS_FERNET_ENCRYPTION_KEY)
    return f.encrypt(f"{budget_code}:{admin_number}:{pas_number}".encode()).decode()


def decrypt(encrypted: str) -> tuple:
    f = Fernet(GPASS_FERNET_ENCRYPTION_KEY)
    admin_pas_numbers = f.decrypt(encrypted.encode(), ttl=60 * 60).decode()
    budget_code, admin_number, pas_number = admin_pas_numbers.split(":", maxsplit=2)

    return budget_code, admin_number, pas_number
