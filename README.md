Focus API
=========

## Introduction

Ontsluiting van de Focus SOAP Api (Online Klantbeeld) middels een json API.

See also (https://dokuwiki.datapunt.amsterdam.nl/doku.php?id=start:focus)

# Requirements

* python 3.6
* docker-compose
* Secure VPN connection (provided by Infra)

# Setup

    # Focus connection parameters
    export FOCUS_USERNAME=
    export FOCUS_PASSWORD=
    export FOCUS_WSDL=<path to wsdl>
    
    # Focus server certificate (not needed in acceptance environment)
    export FOCUS_CERTIFICATE=$(cat ./web/tests/focus.cert.txt)
    
    # TMA certificate to decode the saml token (rattic: "TMA certificaat local")
    # (you can put this line your shell rc file)
    export TMA_CERTIFICATE=<path to certificate>
    
    
The WSDL's for acceptance and production are contained in the web/focus directory

A demo SAML token can be extracted from the tests.
If a SAML token is used this token should be included in the header (x-saml-attribute-token1)

For developing purposes the code in focusserver.py can be changed temporarily from:

    except Exception as error:
            return self._parameter_error_response(error)
            
to:

    except Exception as error:
            bsn = "<BSN nr>"
            
These changes should of course be reversed afterwards.
But in any case, when it is forgotten the Jenkins tests will fail.

The focus WSDL (focus.acc.wsdl) in the project is the WSDL for the acceptance environment.
When moving to production the other WSDL (focus.prd.wsdl) has to be used.

# Rate limiting
By default, there is a rate limit of 5 requests per second for all calls, except for `/status/health` and `/status/data`

See `server.py`


# Developing

    python3 -m venv venv
    pip install -r ./web/requirements.txt
    
Once installed

    source venv/bin/activate

if you save the variables in a local file, e.g. vars.sh then execute

    . vars.sh

NOTE: When running the docker, the path to the WSDL and TMA certificate should be set to
/app/focus/focus.\<acc or prd>.wsdl and /app/focus/tma.cert.txt  #TODO

# Docker

The docker container will start a VPN connection and the web server.

In order to start the VPN server the following two variables should be defined:

    export OPENVPNUSER=
    export OPENVPNUSER_PASSWORD=

The values can be obtained from the infra department or be found in the Openstack configuration for this project.

Use `docker-compose` to start a local Api server.

	docker-compose build
	docker-compose up -d

The API should now be available on http://localhost:8000.
This can be verified by opening http://localhost:8000/status/health.

## Docker tests

    cd ./web/focus/jenkins/test
    docker compose build
    docker run test
    
The docker tests are part of the Jenkins pipeline for this project

# Local

## Testing

    cd ./web
    flake8
    python -m unittest
    
## Code coverage
    
    cd ./web
    coverage erase
    coverage run -m unittest
    coverage report --include=./focus/*.py --fail-under=79
    
Or, for a nice visual presentation of all the covered code:

    coverage html --include=./focus/*.py
    
Open htmlcov/index.html in your browser to see the results

## All tests

In order to run all tests (flake8, unit tests and coverage) run:

    test.sh

NOTE: These tests are also run in the Jenkins pipeline
    
## Local development and testing

    cd ./web
    python -m focus.server
    
The API should now be available on http://localhost:5000.
This can be verified by opening http://localhost:5000/status/health. 

# Urls

All application urls can be found in config.py

# Swagger

Remember to update the swagger.yml in the static directory when updating the API

# Updating dependencies
Direct dependencies are specified in `requirements-root.txt`. These should not have pinned a version (except when needed)

* `pip install -r requirements-root.txt`
* `pip freeze > requirements.txt`
* Add back at the top in requirements.txt
 `--extra-index-url https://nexus.secure.amsterdam.nl/repository/pypi-hosted/simple`

# TMA test certificates were generated with:
`openssl req -x509 -nodes -days 365 -newkey rsa:512 -keyout test_tma_cert.key -out test_tma_cert.crt`

# Fetching WSDL
`curl https://$FOCUS_USERNAME:$FOCUS_PASSWORD@$(grep "<soap:address location=" $FOCUS_WSDL | cut -d '"' -f 2 | cut -d '/' -f 3-)?WSDL -k && echo`
