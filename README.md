![logo](./art/logo_new.jpg)

# ceiling-kat - a web based radio telescope calibration simulation

[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/ska-sa/ceiling-kat?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## Installation


### On a fresh Ubuntu 14.04 machine

run:

    $ sudo apt-get install -y docker.io python-pip git
    $ sudo pip install fig
    $ git clone https://github.com/ska-sa/ceiling-kat
    $ cp fig_example.yml fig.yml
    $ edit fig.yml   # set all the environment variables
    $ fig up -d
    $ fig run django python ./manage.py syncdb   # this will populate the database with empty tables

And answer the questions. Yes, you want to create a superuser.

This will start a webserver on port 80.

## Updating a deployed django_kat

in the root folder run:

    $ git pull
    $ fig build
    $ fig run django python ./manage.py syncdb    # this will update the running database

## Development setup


You need:

   * Python 3
   * Python PIP (`$ sudo apt-get install python3-pip`)
   * RabbitMQ (`$ sudo apt-get install rabbitmq-server`)
   * docker (`$ sudo apt-get install docker.io`)
   * postgres (`$ sudo apt-get install postgresql postgresql-server-dev-all`)

Now to install the requirered libraries run inside the surf_kat folder:

    $ pip3 install -r requirements.txt

Now you are ready to start the pipeline. To start the django server you first need to populate the database:

    $ DJANGO_SETTINGS_MODULE=django_kat.settings.development python3 ./manage.py syncdb

Now you can run a development webserver using:

    $ DJANGO_SETTINGS_MODULE=django_kat.settings.development python3 ./manage.py runserver

To run the scheduled simulations you need to run a broker and celery worker:

    $ make broker &
    $ make worker &

