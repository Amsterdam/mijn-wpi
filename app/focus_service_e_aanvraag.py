import hashlib

from app.e_aanvraag_config import E_AANVRAAG_DOCUMENT_CONFIG, E_AANVRAAG_PRODUCT_NAMES
from app.focus_service_aanvragen import get_client, get_document_url


def get_document_config(document_code_id):
    code_id = str(document_code_id).lower()
    document_config = E_AANVRAAG_DOCUMENT_CONFIG.get(code_id)
    document_config.set("product", document_config.get("product").lower())
    return document_config


def get_steps_collection():
    return {product_name.lower(): [] for product_name in E_AANVRAAG_PRODUCT_NAMES}


def create_e_aanvraag(product_name, steps):

    steps_sorted = sorted(steps, key=lambda d: d["datePublished"])

    raw_id = product_name + steps_sorted[0]["datePublished"]
    id = hashlib.md5(raw_id.encode("utf-8")).hexdigest()

    first_step = steps_sorted[0]  # aanvraag step
    last_step = steps_sorted[-1]  # any step

    date_end = (
        last_step["datePublished"] if last_step["status"] in ["besluit"] else None
    )

    product = {
        "id": id,
        "dateStart": first_step["datePublished"].isoformat(),
        "datePublished": last_step["datePublished"].isoformat(),
        "dateEnd": date_end,
        "decision": last_step["decision"] if date_end else None,
        "status": last_step["step_type"],
        "steps": steps,
    }

    return product


def get_e_aanvraag_step(e_aanvraag, document_code_id, document_config):
    step = {
        "id": document_code_id,
        "title": document_config["document_title"],
        "url": get_document_url(e_aanvraag),
        "datePublished": e_aanvraag["datumDocument"].isoformat(),
        "step_type": document_config["step_type"],
    }

    return step


def get_e_aanvragen(bsn):
    e_aanvragen = []

    try:
        e_aanvragen = get_client().service.EAanvragenTozo(bsn)
    except Exception as error:
        # To Sentry
        return e_aanvragen

    steps_collection = get_steps_collection()

    for e_aanvraag in e_aanvragen:
        document_code_id = e_aanvraag["documentCodeId"]
        document_config = get_document_config(document_code_id)

        if not document_config:
            # Error to Sentry
            continue

        step = get_e_aanvraag_step(e_aanvraag, document_code_id, document_config)

        if step:
            steps_collection[document_config["product"]].append(step)

    aanvragen = []

    for product_name in steps_collection.keys():
        aanvraag = create_e_aanvraag(product_name, steps_collection[product_name])
        aanvragen.append(aanvraag)

    return aanvragen
