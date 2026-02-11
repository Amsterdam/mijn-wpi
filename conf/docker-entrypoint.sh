#!/bin/bash
set -e

# AZ AppService allows SSH into a App instance.
if [ "$MA_CONTAINER_SSH_ENABLED" = "true" ]
then
    echo "Starting SSH ..."
    service ssh start
fi

# see https://unix.stackexchange.com/a/358837 for more info on running uwsgi as www-data user
su -s /bin/bash -c 'uwsgi --uid www-data --gid www-data --ini /api/uwsgi.ini' www-data
