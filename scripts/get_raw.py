import sys
from io import BytesIO

from lxml import etree

from app.config import zeep_config, focus_credentials
from app.old.focusconnect import FocusConnection

focus_connection = FocusConnection(zeep_config, focus_credentials)

bsn = sys.argv[1]


with focus_connection._client.settings(raw_response=True):
    raw_aanvragen = focus_connection._client.service.getAanvragen(bsn=bsn)
    content_bytesio = BytesIO(raw_aanvragen.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
    print(formatted_xml.decode())
    #
    raw_aanvragen = focus_connection._client.service.getJaaropgaven(bsn=bsn)
    content_bytesio = BytesIO(raw_aanvragen.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
    print(formatted_xml.decode())
    #
    raw_aanvragen = focus_connection._client.service.getStadspas(bsn=bsn)
    content_bytesio = BytesIO(raw_aanvragen.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
    print(formatted_xml.decode())
    #
    raw_aanvragen = focus_connection._client.service.getUitkeringspecificaties(bsn=bsn)
    content_bytesio = BytesIO(raw_aanvragen.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
    print(formatted_xml.decode())

    raw_aanvragen = focus_connection._client.service.getEAanvraagTOZO(bsn=bsn)
    content_bytesio = BytesIO(raw_aanvragen.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
    print(formatted_xml.decode())
