import logging
from datetime import date, datetime
from re import sub

from flask.helpers import make_response

from app.config import CONNECTION_ERRORS


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
