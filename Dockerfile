FROM python:3.9.6-buster

MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app

COPY ca/* /usr/local/share/ca-certificates/extras/

RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get autoremove -y \
  && apt-get install --no-install-recommends -y \
  unzip \
  wget \
  dnsutils \
  vim-tiny \
  net-tools \
  netcat \
  libgeos-dev \
  gdal-bin \
  postgresql-client-11 \
  libgdal20 \
  libspatialite7 \
  libfreexl1 \
  libgeotiff2 \
  libwebp-dev \
  proj-bin \
  mime-support \
  gettext \
  && rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old \
  && pip install --upgrade pip \
  && pip install uwsgi \
  && echo "font/woff2    woff2" >> /etc/mime.types \
  && echo "image/webp    webp"  >> /etc/mime.types \
  && chmod -R 644 /usr/local/share/ca-certificates/extras/ \
  && update-ca-certificates \
  && useradd --user-group --system datapunt


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
