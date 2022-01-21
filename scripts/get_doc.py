from io import BytesIO
from sys import argv
import logging.config

from lxml import etree

from app.config_new import config, credentials
from app.focusconnect import FocusConnection

focus_connection = FocusConnection(zeep_config, focus_credentials)


logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {"verbose": {"format": "%(name)s: %(message)s"}},
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "zeep.transports": {
                "level": "DEBUG",
                "propagate": True,
                "handlers": ["console"],
            },
        },
    }
)

bsn = argv[1]
docid = argv[2]

isDms = argv[3]
isBulk = argv[4]

print("Getting doc", bsn, docid, isDms, isBulk)

with focus_connection._client.settings(
    raw_response=True, extra_http_headers={"Accept": "application/xop+xml"}
):
    raw_doc = focus_connection._client.service.getDocument(
        id=docid, bsn=bsn, isBulk=isBulk, isDms=isDms
    )
    content_bytesio = BytesIO(raw_doc.content)
    tree = etree.parse(content_bytesio)
    formatted_xml = etree.tostring(tree, pretty_print=True)
