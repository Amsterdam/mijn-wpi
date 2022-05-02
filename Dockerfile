FROM amsterdam/python:3.9.6-slim-bullseye-minimal

WORKDIR /api

RUN apt-get update
RUN apt-get -y install locales
RUN sed -i -e 's/# nl_NL.UTF-8 UTF-8/nl_NL.UTF-8 UTF-8/' /etc/locale.gen && \
  locale-gen
ENV LANG nl_NL.UTF-8
ENV LANGUAGE nl_NL:nl
ENV LC_ALL nl_NL.UTF-8

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
