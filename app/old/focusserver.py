""" Focus Server

This module represents the Focus API Server
The server uses the Focus connection class to handle the physical connection with the underlying Focus SOAP API
The server interprets requests, execute the corresponding action and return JSON responses
"""
from http.client import NOT_FOUND
from flask import make_response, request

from app.utils import volledig_administratienummer

from app.gpass_service import get_stadspassen


class FocusServer:
    def __init__(self, focus_connection):
        """
        Initializes the Server
        :param focus_connection: The connection to use to access the underlying Focus SOAP API
        :param tma_certificate: The certificate to use to decode SAML tokens (BSN)
        """
        self._focus_connection = focus_connection

    def aanvragen(self, bsn):
        """
        Gets all running and past aanvragen for the BSN that is encoded in the header SAML token
        :return:
        """

        return self._focus_connection.aanvragen(bsn=bsn, url_root=request.script_root)

    def _collect_stadspas_data(self, bsn):
        # 2 stage, first get admin number from focus, then data from gpass
        stadspas_data = self._focus_connection.stadspas(bsn=bsn)

        if not stadspas_data:
            return []

        stadspas_admin_number = volledig_administratienummer(
            stadspas_data["adminstratienummer"]
        )

        if not stadspas_admin_number:
            return []

        stadspassen = get_stadspassen(admin_number=stadspas_admin_number)

        return {"stadspassen": stadspassen, "type": stadspas_data["type"]}

    def combined(self, bsn):
        """Gets all jaaropgaven for the BSN that is encoded in the header SAML token."""

        jaaropgaven = self._focus_connection.jaaropgaven(
            bsn=bsn, url_root=request.script_root
        )
        uitkeringsspec = self._focus_connection.uitkeringsspecificaties(
            bsn=bsn, url_root=request.script_root
        )
        tozo_documents = self._focus_connection.EAanvragenTozo(
            bsn=bsn, url_root=request.script_root
        )
        stadspas = self._collect_stadspas_data(bsn)

        return {
            "jaaropgaven": jaaropgaven,
            "uitkeringsspecificaties": uitkeringsspec,
            "tozodocumenten": tozo_documents,
            "stadspassaldo": stadspas,
        }

    def document(self, bsn):
        """
        Gets a specific aanvraag document for the BSN that is encoded in the header SAML token
        The document is identified by its id and whether it is a bulk or document management document (request args)
        :return:
        """
        id = request.args.get("id", None)
        isBulk = request.args.get("isBulk", "false").lower() == "true"
        isDms = request.args.get("isDms", "false").lower() == "true"

        document = self._focus_connection.document(
            bsn=bsn, id=id, isBulk=isBulk, isDms=isDms
        )

        # Craft a manual request instead
        response = make_response(document["contents"])
        response.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{document["fileName"]}"'  # make sure it is a download
        response.headers["Content-Type"] = document["mime_type"]

        return response
