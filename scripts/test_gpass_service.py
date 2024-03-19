import sys

from app.gpass_service import get_stadspassen
from app.zorgned_service import get_clientnummer, volledig_clientnummer

bsn = None
if len(sys.argv) >= 2:
    bsn = sys.argv[1]

clientnummer = get_clientnummer(bsn)

if clientnummer is not None:
    stadspassen = get_stadspassen(volledig_clientnummer(clientnummer), "M")
    print(stadspassen)

print("geen client nummer")
