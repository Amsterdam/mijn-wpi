import sys

from bs4 import BeautifulSoup

from focus.config import config, credentials
from focus.focusconnect import FocusConnection

focus_connection = FocusConnection(config, credentials)

bsn = sys.argv[1]

aanvragen = focus_connection.aanvragen(bsn=bsn, url_root='/')
jaaropvragen = focus_connection.jaaropgaven(bsn=bsn, url_root='/')
uitkeringsspecificaties = focus_connection.uitkeringsspecificaties(bsn=bsn, url_root='/')

print(f"Aanvragen: {len(aanvragen)}.  jaaropgaven: {len(jaaropvragen)}  uitkeringsspecificaties: {len(uitkeringsspecificaties)}\n",)

commands = []

for i in aanvragen + jaaropvragen + uitkeringsspecificaties:
    print("id:", i['id'])
    print("type:", i['type'])
    print("url:", i['url'])
    docId = i["id"]
    # /focus/document?id=2222&isBulk=false&isDms=false
    isBulk = i['url'].split('&')[1].split('=')[1]
    isDms = i['url'].split('&')[2].split('=')[1]
    command = f'python focus/scripts/get_doc.py {bsn} {docId} {isDms} {isBulk}'
    print("command:", command)

    with focus_connection._client.settings(raw_response=True, extra_http_headers={'Accept': 'application/xop+xml'}):
        raw_doc = focus_connection._client.service.getDocument(id=docId, bsn=bsn, isBulk=isBulk, isDms=isDms)
        tree = BeautifulSoup(raw_doc.content, features="lxml-xml")
        data =tree.find('dataHandler')
        filedata = str(data.text)
        print("data?", bool(filedata), '           ', filedata[:20], ' ... ', filedata[-10:])
        print("\n\n")
