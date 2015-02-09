#!/bin/bash

# !!! ALWAYS CHANGE SETTINGS BELOW !!!
#
export SERVER_NAME=192.168.59.103
export SERVER_PORT=80
export ADMIN_EMAIL="root@localhost"
export SECRET_KEY="SOME RANDOM STRING"


export DEBUG=false
export ALLOWED_HOST=${SERVER_NAME}
export CYBERSKA_URI=http://${SERVER_NAME}:8081/v1/viz
export REDIRECT_URI=http://${SERVER_NAME}:8080/pureweb

fig up -d
