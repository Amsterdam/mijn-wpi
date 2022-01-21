from app.config import FOCUS_WSDL
from app.focus_service import get_client

import operator

client = get_client()

print(client)

for service in client.wsdl.services.values():
    print("service:", service.name)

    for port in service.ports.values():
        operations = sorted(
            port.binding._operations.values(), key=operator.attrgetter("name")
        )

        for operation in operations:
            print("method :", operation.name)
            print("  input :", operation.input.signature())
            print("  output:", operation.output.signature())
