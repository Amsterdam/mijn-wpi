from sys import argv

from app.focus_service_get_document import get_document

bsn = argv[1]
id = argv[2]

isDms = True if argv[3] == "True" else False
isBulk = True if argv[4] == "True" else False

print("Getting doc", bsn, id, isDms, isBulk)

doc = get_document(bsn, id, isBulk, isDms)

print(doc)
