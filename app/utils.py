from cryptography.fernet import Fernet

from app.config import GPASS_FERNET_ENCRYPTION_KEY
import os
from datetime import date, datetime
from functools import wraps

import yaml
from flask import g, request
from flask.helpers import make_response
from openapi_core import create_spec
from openapi_core.contrib.flask import FlaskOpenAPIRequest, FlaskOpenAPIResponse
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator
from tma_saml import (
    HR_KVK_NUMBER_KEY,
    SamlVerificationException,
    get_digi_d_bsn,
    get_e_herkenning_attribs,
)
from tma_saml.tma_saml import get_user_type
from tma_saml.user_type import UserType
from yaml import load

from app.config import (
    BASE_PATH,
    ENABLE_OPENAPI_VALIDATION,
)

openapi_spec = None


def get_tma_certificate():

    tma_certificate = g.get("tma_certificate", None)

    if not tma_certificate:
        tma_cert_location = os.getenv("TMA_CERTIFICATE")

        if tma_cert_location:
            with open(tma_cert_location, "r") as f:
                tma_certificate = g.tma_certificate = f.read()

    return tma_certificate


def get_bsn_from_request():
    """
    Get the BSN based on a request, expecting a SAML token in the headers
    """
    # Load the TMA certificate
    tma_certificate = get_tma_certificate()

    # Decode the BSN from the request with the TMA certificate
    bsn = get_digi_d_bsn(request, tma_certificate)
    return bsn


def get_kvk_number_from_request():
    """
    Get the KVK number from the request headers.
    """
    # Load the TMA certificate
    tma_certificate = get_tma_certificate()

    # Decode the BSN from the request with the TMA certificate
    attribs = get_e_herkenning_attribs(request, tma_certificate)
    kvk = attribs[HR_KVK_NUMBER_KEY]
    return kvk


def get_tma_user():
    user_type = get_user_type(request, get_tma_certificate())
    user_id = None

    if user_type is UserType.BEDRIJF:
        user_id = get_kvk_number_from_request()
    elif user_type is UserType.BURGER:
        user_id = get_bsn_from_request()
    else:
        raise SamlVerificationException("TMA user type not found")

    if not user_id:
        raise SamlVerificationException("TMA user id not found")

    return {"id": user_id, "type": user_type}


def verify_tma_user(function):
    @wraps(function)
    def verify(*args, **kwargs):
        get_tma_user()
        return function(*args, **kwargs)

    return verify


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
