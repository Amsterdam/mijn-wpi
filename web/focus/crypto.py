from cryptography.fernet import Fernet

from focus.config import get_key


def encrypt(budget_code: str, admin_number: str, pas_number) -> str:
    f = Fernet(get_key())
    return f.encrypt(f"{budget_code}:{admin_number}:{pas_number}".encode()).decode()


def decrypt(encrypted: str) -> tuple:
    f = Fernet(get_key())
    admin_pas_numbers = f.decrypt(encrypted.encode(), ttl=60 * 60).decode()
    budget_code, admin_number, pas_number = admin_pas_numbers.split(":", maxsplit=2)

    return budget_code, admin_number, pas_number
