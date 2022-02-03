import json
from app.config import FOCUS_WSDL
from app.focus_service_aanvragen import get_client

import operator

from app.focus_service_stadspas_admin import get_stadspas_admin_number

bsn = ""

client = get_client()

print(client)

for service in client.wsdl.services.values():
    print("service:", service.name)

    for port in service.ports.values():
        operations = sorted(
            port.binding._operations.values(), key=operator.attrgetter("name")
        )

        for operation in operations:
            print("method  :", operation.name)
            print("  input :", operation.input.signature())
            print("  output:", operation.output.signature())


focus_stadspas = client.service.getStadspas(bsn=bsn)
print(json.dumps(focus_stadspas, indent=4))

e_aanvragen = client.service.EAanvragenTozo(bsn=bsn)
print(json.dumps(e_aanvragen, indent=4))
