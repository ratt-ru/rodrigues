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


Development setup
-----------------

You need:

   * Python 3
   * Python PIP (`$ apt-get install python3-pip`)
   * RabbitMQ (`$ apt-get install rabbitmq-server`)
   * docker (`$ apt-get install docker.io`)

Now to install the requirered libraries run inside the surf_kat folder:

   $ pip3 install -r requirements.txt
   
Now you are ready to start the pipeline. To start the django server you first need to populate the database:

    $ DJANGO_SETTINGS_MODULE=surf_kat.settings.development ./manage.py syncdb
   
Now you can run a development webserver using:

    $ DJANGO_SETTINGS_MODULE=surf_kat.settings.development ./manage.py runserver
   
To run the scheduled simulations you need to run a broker and celery worker:

    $ make broker &
    $ make worker &
   
