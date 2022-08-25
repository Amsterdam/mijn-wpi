#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

python /code/manage.py runserver 0.0.0.0:8000
uwsgi --uid www-data --gid www-data --ini /api/uwsgi.ini