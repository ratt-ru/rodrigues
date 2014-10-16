Django based simulation schedular
=================================

Installation
------------

Install Docker:

    https://docs.docker.com/installation/

install fig:

    http://www.fig.sh/install.html

checkout the git repo:

    $ git clone https://github.com/ska-sa/ceiling-kat
    $ cd ceiling-kat/surf_kat

open fig.yml and under django, environment set:

    SECRET_KEY
    HOSTNAME

and then run:

    $ fig up -d
    $ fig run django python ./manage.py syncdb   # this will populate the database with empty tables

And answer the questions. Yes, you want to create a superuser.

This will start a webserver on port 80.


Updating a deployed surf_kat
----------------------------

in the surf_kat folder run:

    $ git pull
    $ fig stop
    $ fig up -d
    $ fig run django python ./manage.py syncdb    # this will update the running database
