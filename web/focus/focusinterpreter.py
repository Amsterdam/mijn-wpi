""" Focus Interpreter

This module interprets Focus responses, e.g. translates integer strings into integers.
See also the convert_aanvragen method for a more detailed explanation.

"""
import logging

from focus.config import urls
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def _to_int(obj, key):
    return _to_type(obj, key, lambda s: int(s))


def _to_bool(obj, key):
    return _to_type(obj, key, lambda s: s.lower() == "true")


def _to_list(obj, key):
    """converts the value of obj[key] to an array
    Example: { "x": 5 } => { "x": [5] }
    :param obj: The object to manipulate
    :param key: The key of the property to convert its value into a list
    :return:
    """
    value = obj.get(key, [])
    if not isinstance(value, list):
        value = [value]
    obj[key] = value
    return obj


def _to_type(obj, key, type_convert):
    """converts the value of obj[key] to the specified type (to_int or to_bool)
    Example: { "x": "5" }, to_int  => { "x": 5 }
    :param obj: The object to manipulate
    :param key: The key of the property to convert
    :param type_convert: The conversion method; lambda s: value
    :return: The object
    """
    value = obj.get(key, None)
    if value is not None:
        obj[key] = type_convert(value)
    return obj


def _get_document_ref(document, url_root="/"):
    """
    Get the API reference for the document
    :param document: the document object
    :param url_root: the root of the url
    :return: a complete API ref to obtain the details of the document
             e.g. "/focus/document?id=12&isBulk=true&isDms=false"
    """
    return "{}?id={}&isBulk={}&isDms={}".format(
        url_root + urls["document"][1:],
        document["id"],
        document["isBulk"],
        document["isDms"],
    )


def _convert_document(document, url_root):
    """
    Convert a document by interpreting properties as ints and bools
    And provide for a ref to the document
    :param document: the document object
    :param url_root: the root of the url
    :return: None
    """
    document["$ref"] = _get_document_ref(document, url_root)
    _to_int(document, "id")
    _to_bool(document, "isBulk")
    _to_bool(document, "isDms")


def _convert_product(product, url_root):
    """
    Convert a product by interpreting properties as ints
    Also provide for the most recent processtap
    :param product: the product to convert
    :param idx_product: the unique index of the product
    :param url_root: the root of the url
    :return: None
    """
    # Process steps
    STAPPEN = ["aanvraag", "inBehandeling", "herstelTermijn", "beslissing", "bezwaar"]

    most_recent = None
    _to_int(product, "dienstverleningstermijn")
    _to_int(product, "inspanningsperiode")
    processtappen = product.get("processtappen", {})
    for idx_stap, stap in enumerate(STAPPEN):
        processtap = processtappen.get(stap, None)
        if processtap is not None:
            processtap["_id"] = idx_stap
            if most_recent is None or processtap["datum"] >= processtappen[most_recent]["datum"]:
                # Take most recent step. When equal highest id goes before any lower id
                most_recent = stap
            _to_list(processtap, "document")
            for document in processtap["document"]:
                _convert_document(document, url_root)
    product["_meest_recent"] = most_recent


def convert_aanvragen(aanvragen, url_root):
    """Convert the aanvragen response to a uniformly formatted object
    When converting SOAP to json arrays of only one value gets translated into an object
    Also, strings with integer or boolean values remain string values
    This method corrects these faulty conversions
    One important correction is to convert objects into arrays. This happens when the collection contains
    only one element. The conversion then converts it into an object (xml does not know about arrays).
    In order to provide for a consistent response these objects are converted into one element lists (object_to_array)
    Each element in any array is given an _id property if an id property is missing in the source data
    :param aanvragen: The aanvragen response object as received from the Focus API
    :param url_root: This value is used to construct a reference to the associating documents
    :return: The aanvragen response object
    """
    # Remove the BSN number from the response!
    # from pprint import pprint
    # pprint(aanvragen)
    del aanvragen["bsn"]

    # Return the list of aanvraag producten
    producten = []

    try:
        # Type corrections
        _to_list(aanvragen, "soortProduct")
        for idx_soort_product, soort_product in enumerate(aanvragen["soortProduct"]):
            _to_list(soort_product, "product")
            for idx_product, product in enumerate(soort_product["product"]):
                product["_id"] = f"{idx_soort_product}-{idx_product}"
                product["soortProduct"] = soort_product["naam"]
                _convert_product(product, url_root)
                producten.append(product)
    except Exception as error:
        logger.error('Failed to convert aanvragen: {}'.format(str(error)))
        raise error

    stappen = [len(product['processtappen']) for product in producten if 'processtappen' in product]
    print("Aantal producten: %i, Stappen: %i" % (len(producten), sum(stappen)))
    return producten


# {
#  title: string | ReactNode;
#  datePublished: string;
#  id: string;
#  url: string;
#  type: FocusInkomenSpecificatieType;
#  isAnnualStatement: boolean;
# }
# FocusInkomenSpecificatieType =
#   | 'IOAZ'
#   | 'BBS'
#   | 'WKO'
#   | 'IOAW'
#   | 'STIMREG'
#   | 'BIBI'
#   | 'PART'
#   | 'BBZ';
def convert_jaaropgaven(jaaropgaven_xml, document_root):
    jaar_opgaven_list = []
    tree = BeautifulSoup(jaaropgaven_xml, features="lxml-xml")
    documents = tree.find_all('document')
    for doc in documents:
        id = doc.id.text
        url = f"{document_root}?id={id}&isBulk=false&isDms=false"

        new_doc = {
            'title': doc.documentCode.omschrijving.text,
            'datePublished': doc.einddatumDocument.text,
            'id': id,
            'url': url,
            'type': '',  # niet van belang
            'isAnnualStatement': True,
        }
        # print("=====", new_doc)
        jaar_opgaven_list.append(new_doc)

    return jaar_opgaven_list

    # uitkeringspecificatie is maandelijks



def convert_uitkeringspecificaties(uitkeringspec_xml, document_root):
    jaar_opgaven_list = []
    tree = BeautifulSoup(uitkeringspec_xml, features="lxml-xml")
    documents = tree.find_all('document')
    for doc in documents:
        id = doc.id.text
        url = f"{document_root}?id={id}&isBulk=false&isDms=false"

        new_doc = {
            'title': doc.documentCode.omschrijving.text,
            'datePublished': doc.einddatumDocument.text,
            'id': id,
            'url': url,
            'type': '',  # niet van belang
            'isAnnualStatement': True,
        }
        print("=====", new_doc)
        jaar_opgaven_list.append(new_doc)

    return jaar_opgaven_list
