#!/bin/bash

# !!! ALWAYS CHANGE SETTINGS BELOW !!!
#
export SERVER_NAME=127.0.0.1
export ADMIN_EMAIL="root@localhost"
export SECRET_KEY="SOME RANDOM STRING"


export DEBUG=false
export ALLOWED_HOST=${SERVER_NAME}
export CYBERSKA_URI=http://${SERVER_NAME}:8081/v1/viz
export REDIRECT_URI=http://${SERVER_NAME}:8080/pureweb

fig up -d
