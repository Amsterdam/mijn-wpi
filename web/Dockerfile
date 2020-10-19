FROM amsterdam/python:3.8-buster
MAINTAINER datapunt@amsterdam.nl


EXPOSE 8000

WORKDIR /app
# remove this when the 3.8.6-buster image is fixed
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY ./focus /app/focus

COPY test.sh /app
COPY .flake8 /app/
COPY ./tests /app/tests

USER datapunt
CMD uwsgi --ini /app/focus/uwsgi.ini
