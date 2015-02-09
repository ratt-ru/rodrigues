# RODRIGUES - a web based radio telescope calibration simulation

## Installation

### On a fresh Ubuntu 14.04 machine

First make sure you have the latest docker (>= 1.3) installed (not the docker.io package).

https://docs.docker.com/installation/ubuntulinux/#ubuntu-trusty-1404-lts-64-bit

run:

    $ sudo apt-get update
    $ sudo apt-get install -y python-pip git
    $ sudo pip install fig
    $ git clone https://github.com/ska-sa/rodrigues && cd rodrigues
    $ edit run.sh   # set all the environment variables
    $ sudo fig up -d

This will start a webserver on port 80.

## Creating superuser

to login in the web application you need a (super) user:

    $ fig run django python3 manage.py createsuperuser

## Development setup


You need:

   * Python 3
   * Python PIP (`$ sudo apt-get install python3-pip`)
   * RabbitMQ (`$ sudo apt-get install rabbitmq-server`)
   * postgres (`$ sudo apt-get install postgresql postgresql-server-dev-all`)

Now to install the requirered libraries run inside the rodrigues folder:

    $ pip3 install -r requirements.txt

Now you are ready to start the pipeline. To start the django server you first need to populate the database:

    $ DJANGO_SETTINGS_MODULE=rodrigues.settings.development python3 ./manage.py migrate

Now you can run a development webserver using:

    $ DJANGO_SETTINGS_MODULE=rodrigues.settings.development python3 ./manage.py runserver

To run the scheduled simulations you need to run a broker and celery worker:

    $ make broker &
    $ make worker &

