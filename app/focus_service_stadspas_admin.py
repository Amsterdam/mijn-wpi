from app.focus_service_aanvragen import get_client


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
    focus_stadspas = None

    try:
        focus_stadspas = get_client().service.getStadspas(bsn=bsn)
    except Exception as error:
        # To Sentry
        return focus_stadspas

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
