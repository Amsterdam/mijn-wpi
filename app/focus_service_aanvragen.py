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
from app.utils import camel_case, default_if_none

focus_client = None


def get_client():
    global focus_client

    if not focus_client:
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


def get_translation(source_title):
    return FOCUS_TITLE_TRANSLATIONS.get(source_title, source_title)


def get_step_status(step_id):
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
        document_transformed = {
            "id": str(document["id"]),
            "title": get_translation(document["omschrijving"]),
            "url": get_document_url(document),
            "datePublished": step["datum"].isoformat(),
        }

        documents.append(document_transformed)

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
    step["decision"] = (
        camel_case(product_source["typeBesluit"])
        if product_source["typeBesluit"]
        else None
    )

    return step


def transform_step(step_id, step, product_source):
    if step_id == "beslissing":
        step_id = "besluit"

    step_transformed = {
        "id": step_id,
        "status": get_step_status(
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

    if step_id == "besluit":
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

    raw_id = product["naam"] + first_step["datePublished"]
    id = hashlib.md5(raw_id.encode("utf-8")).hexdigest()

    product_transformed = {
        "id": id,
        "title": get_translation(product["naam"]),
        "about": get_translation(product["naam"]),
        "statusId": last_step["id"],
        "decision": camel_case(product["typeBesluit"])
        if product["typeBesluit"]
        else None,
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
    all_aanvragen = []
    aanvragen = []

    try:
        all_aanvragen = get_client().service.getAanvragen(bsn)
    except Exception as error:
        logging.error(error)
        return aanvragen

    for product_group in all_aanvragen["soortProduct"]:
        if product_group["naam"] in FOCUS_PRODUCT_GROUPS_ALLOWED:
            for product_aanvraag in product_group["product"]:
                if product_aanvraag["naam"] in FOCUS_PRODUCTS_ALLOWED:
                    aanvragen.append(product_aanvraag)

    product_aanvragen = [
        transform_product(product_aanvraag) for product_aanvraag in aanvragen
    ]

    return product_aanvragen
