#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x   # print all commands to the terminal

export UWSGI_MODULE="app.server"

# run uwsgi
exec uwsgi --ini uwsgi.ini