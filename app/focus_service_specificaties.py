from app.focus_service_aanvragen import get_client


def get_jaaropgaven(bsn):
    jaaropgaven = []
    try:
        jaaropgaven = get_client().service.getJaaropgaven(bsn)
    except Exception as error:
        # To Sentry
        return jaaropgaven


def get_uitkeringsspecificaties(bsn):
    specificaties = []
    try:
        specificaties = get_client().service.getUitkeringspecificaties(bsn)
    except Exception as error:
        # To Sentry
        return specificaties
