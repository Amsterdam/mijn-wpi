FROM amsterdam/python:3.8-buster
LABEL maintainer=datapunt@amsterdam.nl

WORKDIR /api

# remove this when the 3.8.6-buster image is fixed
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

RUN apt-get update
ENV LC_ALL="nl_NL.UTF-8"
ENV LC_CTYPE="nl_NL.UTF-8"
RUN dpkg-reconfigure locales

COPY requirements.txt /api
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY ./scripts /api/scripts
COPY ./app /api/app

COPY uwsgi.ini /api/
COPY test.sh /api/
COPY .flake8 /api/

USER datapunt
CMD uwsgi --ini /api/uwsgi.ini
