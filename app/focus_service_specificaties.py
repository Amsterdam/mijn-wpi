import logging
from app.focus_service_aanvragen import get_client, get_document_url
from app.utils import handle_soap_service_error


def get_jaaropgaven(bsn):
    jaaropgaven = []
    jaaropgaven_source = []

    try:
        jaaropgaven_source = get_client().service.getJaaropgaven(bsn)
        jaaropgaven_source = jaaropgaven_source["document"]
    except Exception as error:
        handle_soap_service_error(error)
        return jaaropgaven

    for jaaropgave_source in jaaropgaven_source:
        date_published = jaaropgave_source["einddatumDocument"]
        year = date_published.year
        title = jaaropgave_source["documentCode"]["omschrijving"]

        jaaropgave = {
            "datePublished": date_published.isoformat(),
            "id": jaaropgave_source["id"],
            "title": f"{title} {year}",
            "variant": jaaropgave_source["variant"],
            "url": "",
        }
        jaaropgave["url"] = get_document_url(
            {**jaaropgave, "isDms": False, "isBulk": False}
        )
        jaaropgaven.append(jaaropgave)

    return jaaropgaven


def get_uitkeringsspecificaties(bsn):
    specificaties = []
    specificaties_source = []

    try:
        specificaties_source = get_client().service.getUitkeringspecificaties(bsn)
        specificaties_source = specificaties_source["document"]
    except Exception as error:
        handle_soap_service_error(error)
        return specificaties

    for specificatie_source in specificaties_source:
        date_published = specificatie_source["einddatumDocument"]
        year = date_published.year
        month = date_published.strftime("%B")
        title = specificatie_source["documentCode"]["omschrijving"]

        uitkeringsspecificatie = {
            "datePublished": date_published.isoformat(),
            "id": specificatie_source["id"],
            "title": f"{title} {month.title()}-{year}",
            "variant": specificatie_source["variant"],
            "url": "",
        }
        uitkeringsspecificatie["url"] = get_document_url(
            {**uitkeringsspecificatie, "isDms": False, "isBulk": False}
        )
        specificaties.append(uitkeringsspecificatie)

    return specificaties
