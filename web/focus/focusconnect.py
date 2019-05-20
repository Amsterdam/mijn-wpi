""" Focus Connection

This module represents a connection with Focus.
The connection can be established, re-established (reset method)
The connection exposes the aanvragen and document methods of the underlying Focus SOAP API
"""
import re
import logging
import xmltodict
import base64

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport

from focus.focusinterpreter import convert_aanvragen

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
        except Exception as error:
            logger.error('Failed to establish a connection with Focus: {}'.format(str(error)))
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
            xml_aanvragen = re.search(r"<return>.*<\/return>", raw_aanvragen).group(0)
            # Translate the response to a Dictionary
            aanvragen = xmltodict.parse(xml_aanvragen)["return"]
            # Convert dict types for lists, ints and bools
            aanvragen = convert_aanvragen(aanvragen, url_root)

        return aanvragen

    def document(self, bsn, id, isBulk, isDms, isDownload):
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
        # Convert the file contents to a base64 encoded string
        logger.info('keys:' + result.keys())
        document["contents"] = result["dataHandler"] if isDownload else base64.b64encode(result["dataHandler"]).decode('utf-8')
        # Provide for a MIME-type
        document["mime_type"] = "application/pdf" if ".pdf" in document["fileName"] else "application/octet-stream"

        return document
