import sys
from app.gpass_service import get_stadspassen
from app.zorgned_service import get_clientnummer, volledig_clientnummer

bsn = None
if len(sys.argv) >= 2:
    bsn = sys.argv[1]

client_nummer = get_clientnummer(bsn)

stadspassen = get_stadspassen(volledig_clientnummer(client_nummer), "M")

print(client_nummer)
print(stadspassen)
