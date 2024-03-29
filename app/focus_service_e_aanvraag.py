import hashlib
import logging

from app.e_aanvraag_config import (
    E_AANVRAAG_DOCUMENT_CONFIG,
    E_AANVRAAG_PRODUCT_TITLES,
    E_AANVRAAG_STEP_COLLECTION_IDS,
    E_AANVRAAG_STEP_ID_TRANSLATIONS,
    exclude_documents_from_processing,
)
from app.focus_service_aanvragen import get_client, get_document_url
from app.utils import handle_soap_service_error


def get_step_status(step_id):
    return E_AANVRAAG_STEP_ID_TRANSLATIONS.get(step_id, step_id)


def get_document_config(document_code_id):
    code_id = str(document_code_id).replace(" ", "")
    document_config = E_AANVRAAG_DOCUMENT_CONFIG.get(code_id)

    if not document_config or document_config.get("is_active", True) is False:
        return None

    return document_config


def get_steps_collection():
    return {id: [] for id in E_AANVRAAG_STEP_COLLECTION_IDS}


def split_bbz_aanvraag(steps_sorted, split_at_step):
    product_name = "Bbz"

    steps_set_a = []
    steps_set_b = []

    use_step_set_b = False

    for step in steps_sorted:
        if step == split_at_step:
            use_step_set_b = True

        if use_step_set_b:
            steps_set_b.append(step)
        else:
            steps_set_a.append(step)

    aanvraag_a = create_e_aanvraag(product_name, steps_set_a, True, False)

    if use_step_set_b:
        aanvraag_b = create_e_aanvraag(
            product_name,
            steps_set_b,
            True,
        )

        return aanvraag_a + aanvraag_b

    return aanvraag_a


def should_split_bbz_at(steps_sorted, decision_step):
    request_step_after_decision = None
    decision_step_found = False

    for step in steps_sorted:
        if step == decision_step:
            decision_step_found = True
        if decision_step_found and step["id"] == "aanvraag":
            request_step_after_decision = step
            break

    return (request_step_after_decision, decision_step_found)


def create_e_aanvraag(
    product_name, steps, already_splitted=False, aggregate_request_steps=True
):
    steps_sorted = sorted(steps, key=lambda d: d["datePublished"])
    raw_id = product_name + steps_sorted[0]["datePublished"].isoformat()
    id = hashlib.md5(raw_id.encode("utf-8")).hexdigest()
    products = []

    first_step = steps_sorted[0]  # aanvraag step
    last_step = steps_sorted[-1]  # any step

    decision_steps = list(filter(lambda s: "besluit" in s["id"], steps_sorted))
    decision_step = decision_steps[-1] if decision_steps else None  # Last decision step

    # If bbz product, check if there is a request step after decision step, if so, split the steps into 2 e_aanvragen.
    # Determine the first request step after the last decision
    if product_name == "Bbz" and not already_splitted:
        (request_step_after_decision, decision_step_found) = should_split_bbz_at(
            steps_sorted, decision_step
        )
        # The step should be splitted
        if request_step_after_decision:
            return split_bbz_aanvraag(steps_sorted, request_step_after_decision)

        # A decision is found for a historic bbz request, no aggregation needed
        elif decision_step_found:
            aggregate_request_steps = False

    for step in steps_sorted:
        step["datePublished"] = step["datePublished"].isoformat()

    date_end = decision_step["datePublished"] if decision_step else None

    aanvraag_step = None
    other_steps = []

    for step in steps_sorted:
        if step["id"] == "aanvraag" and aggregate_request_steps:
            if not aanvraag_step:
                aanvraag_step = step
            else:
                aanvraag_step["documents"] += step["documents"]
        else:
            other_steps.append(step)

    if aanvraag_step and aggregate_request_steps:
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
        "decision": decision_step.get("decision") if decision_step else None,
        "statusId": last_step["id"],
        "steps": steps,
    }

    products.append(product)

    return products


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


def collect_and_transform_status_steps(e_aanvragen):
    steps_collection = get_steps_collection()

    for e_aanvraag in e_aanvragen:
        document_code_id = e_aanvraag["documentCodes"]["documentCodeId"]
        document_config = get_document_config(document_code_id)

        if document_code_id in exclude_documents_from_processing:
            continue

        if not document_config:
            description = "unknown-description"
            extra = None
            if (
                "documentCodes" in e_aanvraag
                and "documentOmschrijving" in e_aanvraag["documentCodes"]
            ):
                description = e_aanvraag["documentCodes"]["documentOmschrijving"]
                # extra = {"code": document_code_id, "description": description}
            logging.error(
                f"Unknown E_Aanvraag Document encountered {document_code_id} / {description}",
                extra=extra,
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

    return steps_collection


def get_e_aanvragen_raw(bsn):
    e_aanvragen = []

    try:
        response = get_client().service.getEAanvraagTOZO(bsn)
        e_aanvragen = response["documentgegevens"] if response else []
    except Exception as error:
        handle_soap_service_error(error)

    return e_aanvragen


def get_e_aanvragen(bsn):
    e_aanvragen = get_e_aanvragen_raw(bsn)

    if not e_aanvragen:
        return []

    aanvragen = []
    steps_collection = collect_and_transform_status_steps(e_aanvragen)

    for product_name in steps_collection.keys():
        if steps_collection[product_name]:
            aanvraag = create_e_aanvraag(product_name, steps_collection[product_name])
            aanvragen.extend(aanvraag)

    return aanvragen
