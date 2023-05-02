from app.focus_config import (
    FOCUS_STADSPAS_FONDSEN_GROENE_STIP,
    FOCUS_STADSPAS_TYPE_PER_FONDS,
)
from app.focus_service_aanvragen import get_client
from app.gpass_config import GPASS_ADMIN_NUMBER_GEMEENTE_CODE
from app.utils import handle_soap_service_error


def has_groene_stip(fondsen):
    # Client needs to have a "toekenning" of a certain type
    for fonds in fondsen:
        is_toegekend = fonds["besluit"] == "toekenning"
        is_correct_fonds = fonds["soortFonds"] in FOCUS_STADSPAS_FONDSEN_GROENE_STIP

        if is_toegekend and is_correct_fonds:
            return True

    return False


def get_first_pas_type(fondsen):
    pas_type = None

    for fonds in fondsen:
        soort = fonds["soortFonds"]
        besluit = fonds["besluit"]

        if besluit != "toekenning":
            continue

        pas_type = FOCUS_STADSPAS_TYPE_PER_FONDS.get(soort)

        if pas_type:
            return pas_type

    return pas_type


def volledig_administratienummer(admin_number) -> str:
    stadspas_admin_number = str(admin_number).zfill(10)
    stadspas_admin_number = f"{GPASS_ADMIN_NUMBER_GEMEENTE_CODE}{stadspas_admin_number}"
    return stadspas_admin_number


def get_stadspas_admin_number(bsn):
    focus_stadspas = None

    try:
        focus_stadspas = get_client().service.getStadspas(bsn=bsn)
    except Exception as error:
        handle_soap_service_error(error)
        return focus_stadspas

    admin_number = focus_stadspas["administratienummer"] if focus_stadspas else None

    if not admin_number:
        return None

    has_pas = False

    if (
        "fondsen" in focus_stadspas
        and focus_stadspas["fondsen"]
        and "fonds" in focus_stadspas["fondsen"]
        and focus_stadspas["fondsen"]["fonds"]
    ):
        fondsen = focus_stadspas["fondsen"]["fonds"]
        has_pas = has_groene_stip(fondsen)

    if not has_pas:
        return None

    pas_type = get_first_pas_type(fondsen)

    return {
        "admin_number": volledig_administratienummer(admin_number),
        "type": pas_type,
    }
