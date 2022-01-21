FROM amsterdam/python:3.8-buster
LABEL maintainer=datapunt@amsterdam.nl

EXPOSE 8000

WORKDIR /api
# remove this when the 3.8.6-buster image is fixed
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

COPY requirements.txt /api
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY ./app /api/app
COPY ./focus /api/focus

COPY uwsgi.ini /api/
COPY test.sh /api/
COPY .flake8 /api/

USER datapunt
CMD uwsgi --ini /api/uwsgi.ini
