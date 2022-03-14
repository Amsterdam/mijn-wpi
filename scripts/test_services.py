import json
import sys

from app.focus_service_aanvragen import get_aanvragen
from app.focus_service_e_aanvraag import get_e_aanvragen
from app.focus_service_specificaties import get_jaaropgaven, get_uitkeringsspecificaties

bsn = None
if len(sys.argv) >= 2:
    bsn = sys.argv[1]

print("\naanvragen")
aanvragen = get_aanvragen(bsn)
print(json.dumps(aanvragen, indent=4))

print("\nuitkering_specificaties")
uitkering_specificaties = get_uitkeringsspecificaties(bsn)
print(json.dumps(uitkering_specificaties, indent=4))

print("\njaaropgaven")
jaaropgaven = get_jaaropgaven(bsn)
print(json.dumps(jaaropgaven, indent=4))

print("\ne-aanvragen")
e_aanvragen = get_e_aanvragen(bsn)
print(json.dumps(e_aanvragen, indent=4))
