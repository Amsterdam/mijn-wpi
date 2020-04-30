""" Focus Connection

This module represents a connection with Focus.
The connection can be established, re-established (reset method)
The connection exposes the aanvragen and document methods of the underlying Focus SOAP API
"""
import re
import logging
import xmltodict

from requests import Session, ConnectionError
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport

from focus.focusinterpreter import convert_aanvragen, convert_jaaropgaven, convert_uitkeringsspecificaties, convert_e_aanvraag_TOZO

logger = logging.getLogger(__name__)


class FocusConnection:
    """ This class encapsulates the (SOAP) connection with Focus"""

    def __init__(self, config, credentials):
        """
        Initializes the Focus SOAP connection
        :param config: SOAP service configuration
        :param credentials: credentials to use for connecting to the SOAP service
        """
        self._config = config
        self._credentials = credentials
        self._client = self._initialize_client()

    def _initialize_client(self):
        """
        Use the configuration details that have been supplied at object creation time to establish a
        connection to the Focus SOAP API.
        The resulting service should be registered by the caller with the object in self._client
        :return: Object
        """
        logger.info('Establishing a connection with Focus')

        session = Session()
        session.verify = self._config['session_verify']
        session.auth = HTTPBasicAuth(self._credentials['username'], self._credentials['password'])

        timeout = 30    # Timeout period for getting WSDL and operations in seconds

        try:
            transport = Transport(session=session, timeout=timeout, operation_timeout=timeout)

            client = Client(wsdl=self._config['wsdl'], transport=transport)

            return client
        except ConnectionError:
            # do not relog the error, because the error has a object address in it, it is a new error every time.
            logger.error('Failed to establish a connection with Focus: Connection Time Out')
            return None
        except Exception as error:
            logger.error('Failed to establish a connection with Focus: {} {}'.format(type(error), str(error)))
            return None

    def reset(self):
        self._client = self._initialize_client()

    def is_alive(self):
        """
        Tells whether the connection with Focus is available.
        :return: boolean
        """
        return self._client is not None

    def aanvragen(self, bsn, url_root):
        """
        Retrieve the aanvragen from Focus
        :param bsn: string
        :param url_root: string: Used to construct href for corresponding documents
        :return: Dictionary
        """

        with self._client.options(raw_response=True):
            # Get raw response as string remove any newlines
            raw_aanvragen = self._client.service.getAanvragen(bsn=bsn).content.decode("utf-8").replace("\n", "")
            # Get the return component out of the SOAP message
            result = re.search(r"<return>.*<\/return>", raw_aanvragen)
            if not result:
                # This can return something else apparently. Lets log this so we can debug this.
                logger.error("no body? %s" % raw_aanvragen)
                return []
            xml_aanvragen = result.group(0)
            # Translate the response to a Dictionary
            aanvragen = xmltodict.parse(xml_aanvragen)["return"]
            # Convert dict types for lists, ints and bools
            aanvragen = convert_aanvragen(aanvragen, url_root)

        return aanvragen

    def jaaropgaven(self, bsn, url_root):
        with self._client.options(raw_response=True):
            raw_jaaropgaven = self._client.service.getJaaropgaven(bsn=bsn).content.decode("utf-8").replace("\n", "")
            result = re.search(r"<return>.*<\/return>", raw_jaaropgaven)
            if not result:
                # This can return something else apparently. Lets log this so we can debug this.
                logger.error("no body jaaropgaven? %s" % raw_jaaropgaven)
                return []
            xml_jaaropgaven = result.group(0)
            jaaropgaven = convert_jaaropgaven(xml_jaaropgaven, url_root)
            return jaaropgaven

    def uitkeringsspecificaties(self, bsn, url_root):
        with self._client.options(raw_response=True):
            raw_specificaties = self._client.service.getUitkeringspecificaties(bsn=bsn).content.decode("utf-8").replace("\n", "")
            result = re.search(r"<return>.*<\/return>", raw_specificaties)
            if not result:
                # This can return something else apparently. Lets log this so we can debug this.
                logger.error("no body uitkeringspec? %s" % raw_specificaties)
                return []
            xml_uitkeringspec = result.group(0)
            uitkeringsspecificaties = convert_uitkeringsspecificaties(xml_uitkeringspec, url_root)
            return uitkeringsspecificaties

    def EAanvragenTozo(self, bsn, url_root):
        with self._client.options(raw_response=True):

            raw_specificaties = self._client.service.getEAanvraagTOZO(bsn=bsn).content.decode("utf-8").replace("\n", "")
            result = re.search(r"<return>.*<\/return>", raw_specificaties)
            if not result:
                # This can return something else apparently. Lets log this so we can debug this.
                logger.error("no body getEAanvraagTOZO? %s" % raw_specificaties)
                return []
            xml = result.group(0)
            tozo_documenten = convert_e_aanvraag_TOZO(xml, url_root)
            return tozo_documenten

    def document(self, bsn, id, isBulk, isDms):
        """
        Retrieve a document from Focus
        :param bsn: string
        :param id: integer
        :param isBulk: boolean
        :param isDms: boolean
        :return: Dictionary
        """

        # Get the document
        result = self._client.service.getDocument(id=id, bsn=bsn, isBulk=isBulk, isDms=isDms)

        # Convert the result to a dictionary for the specified keys
        document = dict([(attr, result[attr]) for attr in ["description", "fileName"]])
        document["contents"] = result["dataHandler"]
        # Provide for a MIME-type
        document["mime_type"] = "application/pdf" if ".pdf" in document["fileName"] else "application/octet-stream"

        return document
