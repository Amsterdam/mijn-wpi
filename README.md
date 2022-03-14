Mijn-WPI API
=========

## Introductie

Deze api levert de volgende data:

- Stadspasaanvragen met bijbehorende status updates.
- Bijstandsuitkeringaanvragen met bijbehorende status updates.
- Aanvragen voor Tozo 1-5, Bbz en TONK met bijbehorende status updates.
- Informatie over stadspassen en de bijbehorende budgetten.

### Kenmerken
- De Bronsystemen zijn Focus (Soap Api) en Gpass (Json Api)
- Alle bronsystemen worden vergaard op basis van een BSN.
- De output van de api is JSON formaat.
- De api is gemodelleerd op basis van OpenAPI 3.x specificatie.

### Development & testen
- Er is geen uitgebreide lokale set-up waarbij ontwikkeld kan worden op basis van een "draaiende" api. Dit zou gemaakt / geïmplementeerd moeten worden.
- Alle tests worden dichtbij de geteste functionaliteit opgeslagen. B.v `some_service.py` en wordt getest in `test_some_service.py`.

### CI/CD
- Bouwen en deployen van de api gebeurt in Jenkins en Openstack.
- De applicatie wordt opgebouwd en deployed via Docker.
