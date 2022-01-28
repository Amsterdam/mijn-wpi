import sys

from bs4 import BeautifulSoup

from app.config import zeep_config, focus_credentials
from app.old.focusconnect import FocusConnection

focus_connection = FocusConnection(zeep_config, focus_credentials)

bsn = sys.argv[1]

aanvragen = focus_connection.aanvragen(bsn=bsn, url_root="/")
jaaropvragen = focus_connection.jaaropgaven(bsn=bsn, url_root="/")
uitkeringsspecificaties = focus_connection.uitkeringsspecificaties(
    bsn=bsn, url_root="/"
)
tozo_documents = focus_connection.EAanvragenTozo(bsn=bsn, url_root="/")

print(
    f"Aanvragen: {len(aanvragen)}.  jaaropgaven: {len(jaaropvragen)}  uitkeringsspecificaties: {len(uitkeringsspecificaties)}\n",
)

commands = []

for i in aanvragen:  # noqa C901
    naam = i["naam"]
    processtappen = i["processtappen"]
    type = f"{i['soortProduct']} - {i['typeBesluit']}"
    print(f"Naam: {naam}")
    print(f"type: {type}")
    print("documenten: ", len(processtappen))
    for stap_naam in processtappen.keys():
        stap = processtappen[stap_naam]
        if stap and "document" in stap and stap["document"]:
            doc_list = stap["document"]
            for doc in doc_list:
                docId = doc["id"]
                isBulk = doc["isBulk"]
                isDms = doc["isDms"]
                print("  id:", docId)
                print("  omschrijving:", doc["omschrijving"])
                print("  url:", doc["$ref"])
                command = (
                    f"python focus/scripts/get_doc.py {bsn} {docId} {isDms} {isBulk}"
                )
                print("  command:", command)
                with focus_connection._client.settings(
                    raw_response=True,
                    extra_http_headers={"Accept": "application/xop+xml"},
                ):
                    raw_doc = focus_connection._client.service.getDocument(
                        id=docId, bsn=bsn, isBulk=isBulk, isDms=isDms
                    )
                    tree = BeautifulSoup(raw_doc.content, features="lxml-xml")
                    data = tree.find("dataHandler")
                    try:
                        filedata = str(data.text)
                        print(
                            "  data?",
                            bool(filedata),
                            "           ",
                            filedata[:20],
                            " ... ",
                            filedata[-10:],
                        )
                    except Exception as e:
                        print("  data?", False, "           ", type(e), e)
                    print("\n\n")

for i in jaaropvragen + uitkeringsspecificaties + tozo_documents:
    print("id:", i["id"])
    print("type:", i["type"])
    print("url:", i["url"])
    docId = i["id"]
    # /focus/document?id=2222&isBulk=false&isDms=false
    isBulk = i["url"].split("&")[1].split("=")[1]
    isDms = i["url"].split("&")[2].split("=")[1]
    command = f"python focus/scripts/get_doc.py {bsn} {docId} {isDms} {isBulk}"
    print("command:", command)

    with focus_connection._client.settings(
        raw_response=True, extra_http_headers={"Accept": "application/xop+xml"}
    ):
        raw_doc = focus_connection._client.service.getDocument(
            id=docId, bsn=bsn, isBulk=isBulk, isDms=isDms
        )
        tree = BeautifulSoup(raw_doc.content, features="lxml-xml")
        data = tree.find("dataHandler")
        try:
            filedata = str(data.text)
            print(
                "data?",
                bool(filedata),
                "           ",
                filedata[:20],
                " ... ",
                filedata[-10:],
            )
        except Exception as e:
            print("data?", False, "           ", type(e), e)
        print("\n\n")
