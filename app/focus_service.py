import logging
from requests import ConnectionError, Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.transports import Transport

from app.config import API_REQUEST_TIMEOUT, FOCUS_PASSWORD, FOCUS_USERNAME, FOCUS_WSDL

focus_client = None


def get_client():
    global focus_client

    if not focus_client:
        logging.info("Establishing a connection with Focus OnlineKlantBeeld")

        session = Session()
        session.auth = HTTPBasicAuth(FOCUS_USERNAME, FOCUS_PASSWORD)

        transport = Transport(
            timeout=API_REQUEST_TIMEOUT,
            operation_timeout=API_REQUEST_TIMEOUT,
            session=session,
        )

        try:

            client = Client(
                wsdl=FOCUS_WSDL,
                transport=transport,
                settings=Settings(xsd_ignore_sequence_order=True, strict=False),
            )

            focus_client = client

            return client

        except ConnectionError as e:
            # do not rethrow the error, because the error has a object address in it, it is a new error every time.
            logging.error(
                f"Failed to establish a connection with Focus: Connection Timeout ({type(e)})"
            )
            return None
        except Exception as error:
            logging.error(
                "Failed to establish a connection with Focus: {} {}".format(
                    type(error), str(error)
                )
            )
            return None

    return focus_client


def get_service(service_name: str):
    client = get_client(service_name)
    try:
        return client.service
    except Exception:
        return None
