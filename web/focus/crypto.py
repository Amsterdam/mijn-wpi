from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

from focus.config import get_key


def encrypt(plain_text: str) -> str:
    f = Fernet(get_key())
    return f.encrypt(f"{plain_text}".encode()).decode()


def decrypt(encrypted: str) -> str:
    f = Fernet(get_key())
    value = f.decrypt(encrypted.encode(), ttl=60 * 60).decode()

    return value
