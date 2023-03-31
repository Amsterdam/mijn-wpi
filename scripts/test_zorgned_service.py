import sys
from app.zorgned_service import get_clientnummer

bsn = None
if len(sys.argv) >= 2:
    bsn = sys.argv[1]

client_nummer = get_clientnummer(bsn)

print(client_nummer)
