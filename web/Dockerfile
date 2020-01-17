FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /app


COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY ./focus /app/focus

COPY test.sh /app
COPY .flake8 /app/
COPY ./tests /app/tests

USER datapunt
CMD uwsgi --ini /app/uwsgi.ini
