import datetime
import logging
import hashlib
from requests import ConnectionError, Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.transports import Transport

from app.config import (
    API_REQUEST_TIMEOUT,
)
from app.focus_config import (
    FOCUS_AANVRAAG_PROCESS_STEPS,
    FOCUS_DOCUMENT_PATH,
    FOCUS_PASSWORD,
    FOCUS_PRODUCT_GROUPS_ALLOWED,
    FOCUS_PRODUCTS_ALLOWED,
    FOCUS_STEP_ID_TRANSLATIONS,
    FOCUS_TITLE_TRANSLATIONS,
    FOCUS_USERNAME,
    FOCUS_WSDL,
)
from app.utils import default_if_none

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


def get_decision(decision):
    return decision.lower().replace(" ", "")


def get_translation(source_title):
    return FOCUS_TITLE_TRANSLATIONS.get(source_title, source_title)


def get_step_title(step_id):
    return FOCUS_STEP_ID_TRANSLATIONS.get(step_id, step_id)


def calculate_municipality_feedback_date_max(
    base_date,
    aantal_dagen_dienstverleningstermijn,
    aantal_dagen_inspanningsperiode,
    aantal_dagen_hersteltermijn=0,
):
    add_days = (
        aantal_dagen_dienstverleningstermijn
        + aantal_dagen_inspanningsperiode
        + aantal_dagen_hersteltermijn
    )

    return base_date + datetime.timedelta(days=add_days)


def calculate_user_feedback_date_max(base_date, aantal_dagen_hersteltermijn):
    return base_date + datetime.timedelta(days=aantal_dagen_hersteltermijn)


def get_document_url(document, url_root="/"):
    return "{}?id={}&isBulk={}&isDms={}".format(
        url_root + FOCUS_DOCUMENT_PATH,
        document["id"],
        document["isBulk"],
        document["isDms"],
    )


def transform_step_documents(step):
    documents = []

    for document in step["document"]:
        document_type = "pdf"  # NOTE: Is this always true?

        step_transformed = {
            "id": str(document["id"]),
            "title": get_translation(document["omschrijving"]),
            "url": get_document_url(document),
            "datePublished": step["datum"].isoformat(),
            "type": document_type,
        }

        return step_transformed

    return documents


def transform_step_hersteltermijn(step, product_source):
    date_aanvraag = product_source["processtappen"]["aanvraag"]["datum"]
    aantal_dagen_hersteltermijn = default_if_none(
        product_source["processtappen"]["herstelTermijn"],
        "aantalDagenHerstelTermijn",
        0,
    )

    # A decision about the request is expected to made before this date
    municipality_decision_date_max = calculate_municipality_feedback_date_max(
        date_aanvraag,
        default_if_none(product_source, "dienstverleningstermijn", 0),
        default_if_none(product_source, "inspanningsperiode", 0),
        aantal_dagen_hersteltermijn,
    )

    # A requester is expected to give feedback to the municipality before this date
    user_feedback_date_max = calculate_user_feedback_date_max(
        date_aanvraag, aantal_dagen_hersteltermijn
    )

    step["dateDecisionExpected"] = municipality_decision_date_max.isoformat()
    step["dateUserFeedbackExpected"] = user_feedback_date_max.isoformat()

    return step


def transform_step_inbehandeling(step, product_source):
    date_aanvraag = product_source["processtappen"]["aanvraag"]["datum"]

    # A decision about the request is expected to made before this date
    municipality_decision_date_max = calculate_municipality_feedback_date_max(
        date_aanvraag,
        default_if_none(product_source, "dienstverleningstermijn", 0),
        default_if_none(product_source, "inspanningsperiode", 0),
    )

    step["dateDecisionExpected"] = municipality_decision_date_max.isoformat()

    return step


def transform_step_besluit(step, product_source):
    # ATTENTION! Chaning the ID of this step
    step["id"] = "besluit"
    step["decision"] = product_source["typeBesluit"]

    return step


def transform_step(step_id, step, product_source):
    step_transformed = {
        "id": step_id,
        "title": get_step_title(
            step_id
        ),  # TODO: Maybe we need more granular determination here by passing more data to determine a better title?
        "documents": transform_step_documents(step),
        "datePublished": step["datum"].isoformat(),
    }

    if step_id == "inBehandeling":
        step_transformed = transform_step_inbehandeling(
            step_transformed, product_source
        )

    if step_id == "herstelTermijn":
        step_transformed = transform_step_hersteltermijn(
            step_transformed, product_source
        )

    if step_id == "beslissing":
        step_transformed = transform_step_besluit(step_transformed, product_source)

    return step_transformed


def transform_product(product):

    steps = []
    decision_step = None

    for step_id in FOCUS_AANVRAAG_PROCESS_STEPS:
        if product["processtappen"][step_id]:
            step = transform_step(step_id, product["processtappen"][step_id], product)
            steps.append(step)

            if step["id"] == "besluit":
                decision_step = step

    first_step = steps[0]  # aanvraag step
    last_step = steps[-1]  # any step

    title = get_translation(product["naam"])
    raw_id = title + first_step["datePublished"]
    id = hashlib.md5(raw_id.encode("utf-8")).hexdigest()

    product_transformed = {
        "id": id,
        "title": title,
        "status": last_step["id"],
        "decision": (
            get_decision(product["typeBesluit"]) if product["typeBesluit"] else None
        ),
        # Last update
        "datePublished": last_step["datePublished"],
        # Date start of the process
        "dateStart": first_step["datePublished"],
        # Date end of the process
        "dateEnd": decision_step["datePublished"] if decision_step else None,
        "steps": steps,
    }

    return product_transformed


def get_aanvragen(bsn):
    all_aanvragen = get_client().service.getAanvragen(bsn)
    aanvragen = []

    for product_group in all_aanvragen["soortProduct"]:
        if product_group["naam"] in FOCUS_PRODUCT_GROUPS_ALLOWED:
            for product_aanvraag in product_group["product"]:
                if product_aanvraag["naam"] in FOCUS_PRODUCTS_ALLOWED:
                    aanvragen.append(product_aanvraag)

    product_aanvragen = [
        transform_product(product_aanvraag) for product_aanvraag in aanvragen
    ]

    return product_aanvragen


def get_document(bsn, id, isBulk, isDms):
    header_value = {"Accept": "application/xop+xml"}

    # Get the document
    document = get_client().service.getDocument(
        id=id, bsn=bsn, isBulk=isBulk, isDms=isDms
    )

    document_content = None

    # tree = BeautifulSoup(raw_document.content, features="lxml-xml")
    # data_element = tree.find("dataHandler")

    # if not data_element:
    #     doc = self._client.service.getDocument(
    #         id=id, bsn=bsn, isBulk=isBulk, isDms=isDms
    #     )
    #     if doc and doc["dataHandler"]:
    #         data = doc["dataHandler"]
    #         filename = doc["fileName"]
    #         logging.error("fallback document method is used")
    #     else:
    #         raise Exception("Requested document is empty")
    # else:
    #     data = data_element.text
    #     data = base64.b64decode(data)
    #     filename = tree.find("fileName").text

    mime_type = (
        "application/pdf"
        if ".pdf" in document["fileName"]
        else "application/octet-stream"
    )

    document = {
        "fileName": document["fileName"],
        "contents": document_content,
        "mime_type": mime_type,
    }

    return document


def has_groene_stip(fondsen):
    # Client needs to have a "toekenning" of a certain type
    for f in fondsen:
        is_toegekend = f.find("besluit").text == "toekenning"
        is_correct_fonds = f.find("soortFonds").text in ["3555", "3556", "3557", "3558"]

        # Temporarily disable check on Toekenning
        # start = parser.isoparse(f.find("dtbegin").text).date()
        # end = parser.isoparse(f.find("dteinde").text).date()
        # is_actueel_besluit = start < today < end
        # if is_toegekend and is_correct_fonds and is_actueel_besluit:

        if is_toegekend and is_correct_fonds:
            return True

    return False


def get_stadspas_admin_number(bsn):
    focus_stadspas = get_client().service.getStadspas(bsn=bsn)
    admin_number = focus_stadspas["administratienummer"]

    if not admin_number:
        return None

    # fondsen = tree.find("fondsen").find_all("fonds", recursive=False)
    fondsen = []
    has_pas = has_groene_stip(fondsen)

    if not has_pas:
        return None

    pas_type = None

    # TODO: Check this code, can we get more than 1 fonds?
    for fonds in fondsen:
        soort = fonds.find("soortFonds").text
        besluit = fonds.find("besluit").text

        if besluit != "toekenning":
            continue

        if soort == "3555":
            pas_type = "hoofpashouder"
        elif soort == "3556":
            pas_type = "partner"
        elif soort == "3557":
            pas_type = "kind"

    return {
        "admin_number": admin_number,
        "type": pas_type,
    }
