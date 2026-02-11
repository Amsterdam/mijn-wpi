#!/bin/bash
set -e

# AZ AppService allows SSH into a App instance.
if [ "$MA_CONTAINER_SSH_ENABLED" = "true" ]
then
    echo "Starting SSH ..."
    service ssh start
fi

uwsgi --ini /api/uwsgi.ini
