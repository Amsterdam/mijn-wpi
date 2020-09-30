from io import BytesIO
from sys import argv

from lxml import etree

from focus.config import config, credentials
from focus.focusconnect import FocusConnection

focus_connection = FocusConnection(config, credentials)


bsn = argv[1]
docid = argv[2]

isDms = argv[3]
isBulk = argv[4]

print("Getting doc", bsn, docid, isDms, isBulk)

with focus_connection._client.settings(raw_response=True):
    raw_doc = focus_connection._client.service.getDocument(id=docid, bsn=bsn, isBulk=isBulk, isDms=isDms)
    content_bytesio = BytesIO(raw_doc.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
    print(formatted_xml.decode())
