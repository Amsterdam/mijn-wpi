import logging
import os
from datetime import date, datetime
from functools import wraps
from re import sub

import yaml
from cryptography.fernet import Fernet
from flask import g, request
from flask.helpers import make_response
from openapi_core import create_spec
from openapi_core.contrib.flask import FlaskOpenAPIRequest, FlaskOpenAPIResponse
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator
from yaml import load

from app.config import BASE_PATH, CONNECTION_ERRORS, ENABLE_OPENAPI_VALIDATION
from app.gpass_config import GPASS_FERNET_ENCRYPTION_KEY

openapi_spec = None


def get_openapi_spec():
    global openapi_spec
    if not openapi_spec:
        with open(os.path.join(BASE_PATH, "openapi.yml"), "r") as spec_file:
            spec_dict = load(spec_file, Loader=yaml.Loader)

        openapi_spec = create_spec(spec_dict)

    return openapi_spec


def validate_openapi(function):
    @wraps(function)
    def validate(*args, **kwargs):

        if ENABLE_OPENAPI_VALIDATION:
            spec = get_openapi_spec()
            openapi_request = FlaskOpenAPIRequest(request)
            validator = RequestValidator(spec)
            result = validator.validate(openapi_request)
            result.raise_for_errors()

        response = function(*args, **kwargs)

        if ENABLE_OPENAPI_VALIDATION:
            openapi_response = FlaskOpenAPIResponse(response)
            validator = ResponseValidator(spec)
            result = validator.validate(openapi_request, openapi_response)
            result.raise_for_errors()

        return response

    return validate


def success_response_json(response_content):
    return make_response({"status": "OK", "content": response_content}, 200)


def error_response_json(message: str, code: int = 500):
    return make_response({"status": "ERROR", "message": message}, code)


def to_date(date_input):
    if isinstance(date_input, date):
        return date_input

    if isinstance(date_input, datetime):
        return date_input.date()

    if "T" in date_input:
        return datetime.strptime(date_input, "%Y-%m-%dT%H:%M:%S").date()

    return datetime.strptime(date_input, "%Y-%m-%d").date()


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


def default_if_none(data, key, default):
    if data and key in data:
        value = data[key]
    return default if value is None else value


def camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def handle_soap_service_error(error):
    error_original = error
    extra_default = {"originalError": error_original}
    extra = None
    error_string = str(error)

    if "No row with the given identifier exists" in error_string:
        extra = extra_default
        error = "No row with the given identifier exists"

    elif filter(lambda err: err in error_string, CONNECTION_ERRORS):
        extra = extra_default
        error = "Focus connection failure"

    logging.error(error, extra=extra)
