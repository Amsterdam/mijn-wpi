from io import BytesIO

from lxml import etree

from focus.config import config, credentials
from focus.focusconnect import FocusConnection

focus_connection = FocusConnection(config, credentials)

bsn = "123456789"


with focus_connection._client.options(raw_response=True):
    raw_aanvragen = focus_connection._client.service.getAanvragen(bsn=bsn)

    content_bytesio = BytesIO(raw_aanvragen.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
    print(formatted_xml.decode())
