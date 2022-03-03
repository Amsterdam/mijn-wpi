import hashlib
import logging

from app.e_aanvraag_config import (
    E_AANVRAAG_DOCUMENT_CONFIG,
    E_AANVRAAG_PRODUCT_TITLES,
    E_AANVRAAG_STEP_COLLECTION_IDS,
    E_AANVRAAG_STEP_ID_TRANSLATIONS,
)
from app.focus_service_aanvragen import get_client, get_document_url


def get_step_status(step_id):
    return E_AANVRAAG_STEP_ID_TRANSLATIONS.get(step_id, step_id)


def get_document_config(document_code_id):
    code_id = str(document_code_id).replace(" ", "")
    document_config = E_AANVRAAG_DOCUMENT_CONFIG.get(code_id)

    if not document_config:
        return None

    return document_config


def get_steps_collection():
    return {id: [] for id in E_AANVRAAG_STEP_COLLECTION_IDS}


def create_e_aanvraag(product_name, steps):
    steps_sorted = sorted(steps, key=lambda d: d["datePublished"])
    raw_id = product_name + steps_sorted[0]["datePublished"].isoformat()
    id = hashlib.md5(raw_id.encode("utf-8")).hexdigest()

    first_step = steps_sorted[0]  # aanvraag step
    last_step = steps_sorted[-1]  # any step
    decision_steps = list(filter(lambda s: s["id"] == "besluit", steps_sorted))
    decision_step = decision_steps[-1] if decision_steps else None  # Last decision step

    for step in steps_sorted:
        step["datePublished"] = step["datePublished"].isoformat()

    date_end = decision_step["datePublished"] if decision_step else None

    aanvraag_step = None
    other_steps = []

    for step in steps_sorted:
        if step["id"] == "aanvraag":
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
        "about": product_name,
        "dateStart": first_step["datePublished"],
        "datePublished": last_step["datePublished"],
        "dateEnd": date_end,
        "decision": decision_step["decision"] if decision_step else None,
        "status": last_step["id"],
        "steps": steps,
    }

    return product


def get_e_aanvraag_document(e_aanvraag, document_config):
    title = document_config["document_title"]

    date_published = e_aanvraag["datumDocument"].isoformat()

    if document_config["step_id"] == "aanvraag":
        display_date_published = e_aanvraag["datumDocument"].strftime("%d %B %Y %H:%M")
        title = f"{title}\n{display_date_published}"  # dd MMMM yyyy

    return {
        "id": str(e_aanvraag["documentId"]),
        "dcteId": e_aanvraag["documentCodes"]["documentCodeId"],
        "title": title,
        "url": get_document_url(
            {
                "isBulk": e_aanvraag["isBulk"],
                "isDms": e_aanvraag["isDms"],
                "id": e_aanvraag["documentId"],
            }
        ),
        "datePublished": date_published,
    }


def get_e_aanvraag_step(e_aanvraag, document_config):
    step_id = document_config["step_id"]
    step = {
        "id": step_id,
        "status": get_step_status(step_id),
        "datePublished": e_aanvraag["datumDocument"],
        "documents": [get_e_aanvraag_document(e_aanvraag, document_config)],
    }

    if document_config.get("about_parent"):
        step["about"] = document_config.get("about")

    decision = document_config.get("decision")
    if decision:
        step["decision"] = decision

    product_specific = document_config.get("about_specific")
    if product_specific:
        step["productSpecific"] = product_specific

    return step


def get_e_aanvragen(bsn):
    e_aanvragen = []

    try:
        response = get_client().service.getEAanvraagTOZO(bsn)
        e_aanvragen = response["documentgegevens"]
    except Exception as error:
        logging.error(error)
        return e_aanvragen

    steps_collection = get_steps_collection()

    for e_aanvraag in e_aanvragen:
        document_code_id = e_aanvraag["documentCodes"]["documentCodeId"]
        document_config = get_document_config(document_code_id)

        if not document_config:
            description = "unknown-description"
            if (
                "documentCodes" in e_aanvraag
                and "documentOmschrijving" in e_aanvraag["documentCodes"]
            ):
                description = e_aanvraag["documentCodes"]["documentOmschrijving"]
            logging.error(
                f"Unknown E_Aanvraag Document encountered {document_code_id} / {description}"
            )
            continue

        step = get_e_aanvraag_step(e_aanvraag, document_config)

        about = (
            document_config["about"]
            if not document_config.get("about_parent")
            else document_config["about_parent"]
        )

        if step:
            steps_collection[about].append(step)

    aanvragen = []

    for product_name in steps_collection.keys():
        aanvraag = create_e_aanvraag(product_name, steps_collection[product_name])
        aanvragen.append(aanvraag)

    return aanvragen
