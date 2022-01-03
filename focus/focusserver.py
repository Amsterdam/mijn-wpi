""" Focus Server

This module represents the Focus API Server
The server uses the Focus connection class to handle the physical connection with the underlying Focus SOAP API
The server interprets requests, execute the corresponding action and return JSON responses
"""
import logging

from flask import jsonify, request, Response, make_response

from .measure_time import MeasureTime
from .gpass_connect import GpassConnection
from .saml import get_bsn_from_request
from requests import ConnectionError

from .config import get_gpass_bearer_token, get_gpass_api_location
from .utils import volledig_administratienummer

logger = logging.getLogger(__name__)


class FocusServer:
    def __init__(self, focus_connection, tma_certificate):
        """
        Initializes the Server
        :param focus_connection: The connection to use to access the underlying Focus SOAP API
        :param tma_certificate: The certificate to use to decode SAML tokens (BSN)
        """
        self._focus_connection = focus_connection
        self._tma_certificate = tma_certificate

    def is_alive(self):
        return self._focus_connection.is_alive()

    def _no_connection_response(self):
        """
        Returns a response telling that the Focus API is not accessible
        Reset the connection so that it will be re-established on the next call
        """
        self._focus_connection.reset()
        return Response(
            "Focus connectivity failed", content_type="text/plain", status=500
        )

    @staticmethod
    def _parameter_error_response(message):
        """
        Returns a response telling that the supplied parameter is incorrect
        """
        return Response(
            "Parameter error: {}".format(message), content_type="text/plain", status=422
        )

    @staticmethod
    def health():
        """
        If the server responds to this message (which is always does) it is considered alive (healthy)
        :return: OK
        """
        return Response("OK", content_type="text/plain")

    def status_data(self):
        """
        If the connection with the Focus SOAP API is alive it is assumed that the data is available
        :return: Response
        """
        try:
            if self._focus_connection.is_alive():
                return Response("Connectivity to Focus OK", content_type="text/plain")
        except Exception:
            pass

        return self._no_connection_response()

    def aanvragen(self):
        """
        Gets all running and past aanvragen for the BSN that is encoded in the header SAML token
        :return:
        """
        try:
            bsn = get_bsn_from_request(request)
        except Exception as error:
            return self._parameter_error_response(error)

        try:
            aanvragen = self._focus_connection.aanvragen(
                bsn=bsn, url_root=request.script_root
            )
        except ConnectionError as error:
            logger.exception(
                "Failed to retrieve aanvragen: {}".format(type(error)), exc_info=error
            )
            return self._no_connection_response()
        except Exception as error:
            logger.exception(
                "Failed to retrieve aanvragen (unknown error): {} {}".format(
                    type(error), str(error)
                ),
                exc_info=error,
            )
            return self._no_connection_response()

        return jsonify(aanvragen)

    def _collect_stadspas_data(self, bsn):
        # 2 stage, first get admin number from focus, then data from gpass
        gpass_con = GpassConnection(get_gpass_api_location(), get_gpass_bearer_token())

        stadspas_data = self._focus_connection.stadspas(bsn=bsn)
        if not stadspas_data:
            return None

        stadspas_admin_number = volledig_administratienummer(
            stadspas_data["adminstratienummer"]
        )

        stadspassen = []
        if stadspas_admin_number:
            stadspassen = gpass_con.get_stadspassen(admin_number=stadspas_admin_number)

        return {"stadspassen": stadspassen, "type": stadspas_data["type"]}

    def combined(self):
        """Gets all jaaropgaven for the BSN that is encoded in the header SAML token."""

        try:
            bsn = get_bsn_from_request(request)
        except Exception as error:
            return self._parameter_error_response(error)

        try:
            with MeasureTime("jaaropgaven"):
                jaaropgaven = self._focus_connection.jaaropgaven(
                    bsn=bsn, url_root=request.script_root
                )
            with MeasureTime("uitkeringspecificaties"):
                uitkeringsspec = self._focus_connection.uitkeringsspecificaties(
                    bsn=bsn, url_root=request.script_root
                )
            with MeasureTime("tozo documenten"):
                tozo_documents = self._focus_connection.EAanvragenTozo(
                    bsn=bsn, url_root=request.script_root
                )
            with MeasureTime("stadspas"):
                stadspas = self._collect_stadspas_data(bsn)

            return {
                "status": "OK",
                "content": {
                    "jaaropgaven": jaaropgaven,
                    "uitkeringsspecificaties": uitkeringsspec,
                    "tozodocumenten": tozo_documents,
                    "stadspassaldo": stadspas,
                },
            }
        except ConnectionError as error:
            logger.exception(
                "Failed to retrieve combined: {}".format(type(error)), exc_info=error
            )
            return self._no_connection_response()
        except Exception as error:
            logger.exception(
                "Failed to retrieve combined (unknown error): {} {}".format(
                    type(error), str(error)
                ),
                exc_info=error,
            )
            return self._no_connection_response()

    def document(self):
        """
        Gets a specific aanvraag document for the BSN that is encoded in the header SAML token
        The document is identified by its id and whether it is a bulk or document management document (request args)
        :return:
        """
        id = request.args.get("id", None)
        isBulk = request.args.get("isBulk", "false").lower() == "true"
        isDms = request.args.get("isDms", "false").lower() == "true"

        try:
            bsn = get_bsn_from_request(request)
        except Exception as error:
            return self._parameter_error_response(error)

        try:
            document = self._focus_connection.document(
                bsn=bsn, id=id, isBulk=isBulk, isDms=isDms
            )
        except ConnectionError as error:
            logger.exception(
                "Failed to retrieve document: {}".format(type(error)), exc_info=error
            )
            return self._no_connection_response()
        except Exception as error:
            logger.exception(
                "Failed to retrieve document: {} {}".format(type(error), str(error)),
                exc_info=error,
            )
            return self._no_connection_response()

        if document is None:
            logger.error(
                f"Document empty. type bsn: {type(bsn)} {len(bsn)}  type id: {type(id)}"
            )
            return "Document not received from source.", 404

        # flask.send_file() won't work with content from memory and uWSGI. It expects a file on disk.
        # Craft a manual request instead
        response = make_response(document["contents"])
        response.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{document["fileName"]}"'  # make sure it is a download
        response.headers["Content-Type"] = document["mime_type"]

        return response
