import datetime


example_response = {
    "administratienummer": 123123123,
    "bsn": 12312312399,
    "fondsen": {
        "fonds": [
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 180572,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 180573,
                "soortFonds": 3557,
            },
        ]
    },
}


example_response2 = {
    "administratienummer": 123123123,
    "bsn": 12312312399,
    "fondsen": {
        "fonds": [
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 384018,
                "soortFonds": 3555,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2018, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2019, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 1609546,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2018, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2019, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 1609547,
                "soortFonds": 3555,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2020, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2021, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 381271,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2019, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2020, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 740599,
                "soortFonds": 3551,
            },
            {
                "besluit": "toekenning",
                "dtbegin": datetime.datetime(2019, 9, 1, 0, 0),
                "dteinde": datetime.datetime(2020, 8, 31, 0, 0),
                "geldigTotEnMet": None,
                "geldigVan": datetime.datetime(1900, 1, 1, 0, 0),
                "id": 757447,
                "soortFonds": 3555,
            },
        ]
    },
}
