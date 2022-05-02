FROM python:3.9.6-buster

LABEL MAINTAINER=datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app

COPY ca/* /usr/local/share/ca-certificates/extras/

RUN apt-get update
RUN apt-get autoremove -y
RUN pip install --upgrade pip
RUN mkdir /usr/local/share/ca-certificates/extras


RUN chmod -R 644 /usr/local/share/ca-certificates/extras/
RUN update-ca-certificates
RUN useradd --user-group --system datapunt

WORKDIR /api

RUN apt-get -y install locales
RUN sed -i -e 's/# nl_NL.UTF-8 UTF-8/nl_NL.UTF-8 UTF-8/' /etc/locale.gen
RUN locale-gen

ENV LANG nl_NL.UTF-8
ENV LANGUAGE nl_NL:nl
ENV LC_ALL nl_NL.UTF-8

COPY requirements.txt /api
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY ./scripts /api/scripts
COPY ./app /api/app

COPY uwsgi.ini /api/
COPY test.sh /api/
COPY .flake8 /api/

USER datapunt
CMD uwsgi --ini /api/uwsgi.ini
