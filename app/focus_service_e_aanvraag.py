import hashlib
import logging

from app.e_aanvraag_config import (
    E_AANVRAAG_DOCUMENT_CONFIG,
    E_AANVRAAG_PRODUCT_NAMES,
    E_AANVRAAG_PRODUCT_TITLES,
)
from app.focus_service_aanvragen import get_client, get_document_url


def get_document_config(document_code_id):
    code_id = str(document_code_id)
    document_config = E_AANVRAAG_DOCUMENT_CONFIG.get(code_id)

    if not document_config:
        return None

    document_config["product"] = document_config.get("product").lower()
    return document_config


def get_steps_collection():
    return {product_name.lower(): [] for product_name in E_AANVRAAG_PRODUCT_NAMES}


def create_e_aanvraag(product_name, steps):
    steps_sorted = sorted(steps, key=lambda d: d["datePublished"])
    raw_id = product_name + steps_sorted[0]["datePublished"].isoformat()
    id = hashlib.md5(raw_id.encode("utf-8")).hexdigest()

    first_step = steps_sorted[0]  # aanvraag step
    last_step = steps_sorted[-1]  # any step

    for step in steps_sorted:
        step["datePublished"] = step["datePublished"].isoformat()

    date_end = last_step["datePublished"] if last_step["title"] in ["besluit"] else None

    aanvraag_step = None
    other_steps = []

    for step in steps_sorted:
        if step["title"] == "aanvraag":
            if not aanvraag_step:
                aanvraag_step = step
            else:
                aanvraag_step["documents"] += step["documents"]
        else:
            other_steps.append(step)

    if aanvraag_step:
        steps = [aanvraag_step] + other_steps
    else:
        steps = other_steps

    product = {
        "id": id,
        "title": E_AANVRAAG_PRODUCT_TITLES.get(product_name, product_name),
        "dateStart": first_step["datePublished"],
        "datePublished": last_step["datePublished"],
        "dateEnd": date_end,
        "decision": last_step["decision"] if date_end else None,
        "status": last_step["title"],
        "steps": steps,
    }

    return product


def get_e_aanvraag_document(e_aanvraag, document_config):
    title = document_config["document_title"]

    date_published = e_aanvraag["datumDocument"].isoformat()

    if document_config["step_type"] == "aanvraag":
        title = f"{title}\n{date_published}"

    return {
        "id": str(e_aanvraag["documentId"]),
        "title": title,
        "url": get_document_url({**e_aanvraag, "id": e_aanvraag["documentId"]}),
        "datePublished": date_published,
    }


def get_e_aanvraag_step(e_aanvraag, document_code_id, document_config):
    step = {
        "id": document_code_id,
        "title": document_config["step_type"],
        "datePublished": e_aanvraag["datumDocument"],
        "documents": [get_e_aanvraag_document(e_aanvraag, document_config)],
    }

    decision = document_config.get("decision")
    if decision:
        step["decision"] = decision

    return step


def get_e_aanvragen(bsn):
    e_aanvragen = []

    try:
        response = get_client().service.getEAanvraagTozo(bsn)
        e_aanvragen = response.get("documentgegevens", [])
    except Exception as error:
        # To Sentry
        return e_aanvragen

    steps_collection = get_steps_collection()

    for e_aanvraag in e_aanvragen:
        document_code_id = e_aanvraag["documentCodes"]["documentCodeId"]
        document_config = get_document_config(document_code_id)

        if not document_config:
            # Error to Sentry
            logging.error(f"Unknown E_Aanvraag Document encountered {document_code_id}")
            continue

        step = get_e_aanvraag_step(e_aanvraag, document_code_id, document_config)

        if step:
            steps_collection[document_config["product"]].append(step)

    aanvragen = []

    for product_name in steps_collection.keys():
        aanvraag = create_e_aanvraag(product_name, steps_collection[product_name])
        aanvragen.append(aanvraag)

    return aanvragen
