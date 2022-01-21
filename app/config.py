""" Configuration

This module contains the configuration details of the application

The actual values are retrieved from shell variables that are stored outside of the application

"""
import os


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_variable(v, default_value=None):
    """Try to read variable, If it fails return None or a specified other default value
    :param v: variable name
    :param default_value: default value if no value can be found
    :return: the variable value
    """
    value = os.getenv(v)
    return value if value is not None else default_value


# def check_env():
#     """
#     Checks if all required environment variables have been set
#     """
#     missing_vars = [
#         v
#         for v in ["FOCUS_USERNAME", "FOCUS_PASSWORD", "FOCUS_WSDL", "TMA_CERTIFICATE"]
#         if not get_variable(v)
#     ]
#     if missing_vars:
#         raise Exception(
#             "Missing environment variables {}".format(", ".join(missing_vars))
#         )


config = {
    "wsdl": get_variable("FOCUS_WSDL"),
    "session_verify": get_variable(
        "FOCUS_CERTIFICATE", False
    ),  # Default don't check the certificate
}

credentials = {
    "username": get_variable("FOCUS_USERNAME"),
    "password": get_variable("FOCUS_PASSWORD"),
}

SENTRY_DSN = get_variable("SENTRY_DSN")

urls = {
    "health": "/status/health",
    "data": "/status/data",
    "aanvragen": "/focus/aanvragen",
    "document": "/focus/document",
    "combined": "/focus/combined",
    "stadspastransacties": "/focus/stadspastransacties/<string:encrypted_admin_pasnummer>",
}


def get_TMA_certificate():
    with open(get_variable("TMA_CERTIFICATE"), "r") as f:
        return f.read()
