# RODRIGUES

RODRIGUES stands for **R**ATT **O**nline **D**econvolved **R**adio **I**mage **G**eneration **U**sing **E**soteric **S**oftware. It is a web based radio telescope simulation and reduction tool. From a technical perspective it is a web based parameterised docker container scheduler with a result set viewer. Hopefully in the future it becomes less radio telescope specific and a more generic comutation scheduler. 

screenshots: http://imgur.com/a/G31yY

## Installation

### On a fresh Ubuntu 14.04 machine

First make sure you have the latest docker (>= 1.3) installed (not the default
Ubuntu docker.io package).

https://docs.docker.com/installation/ubuntulinux/#ubuntu-trusty-1404-lts-64-bit

run:

    $ sudo apt-get update
    $ sudo apt-get install -y python-pip git
    $ sudo pip install docker-compose
    $ git clone https://github.com/ska-sa/rodrigues && cd rodrigues

### running 

To start RODRIGUES:

    $ SECRET_KEY=secretkey SERVER_NAME=localhost docker-compose up

This will start a webserver on port 80. Replace `SECRET_KEY` with something secret and random, it
is used to create HTTP sessions. you can use the `-d` flag to fork
docker-compose to the background.

### configuration

There are more environment variables you may need to set:
 - **SERVER_NAME** (default: rodrigues.meqtrees.net)
 - **DEBUG** set to true to enable debugging mode (default: off)

If things are not working, make sure the SERVER\_NAME matches the
host name you use to connect to rodrigues. If that doesn't help
turn on debug (DEBUG=true) or examine the log files (docker-compose logs).

### Initialise DB

First time you run this app you need to create and populate the database

    $ docker-compose run worker python3 manage.py migrate

### Creating admin user

    $ docker-compose run worker python3 ./manage.py createsuperuser

### Fetching / creating simulation containers

Note that you may need to pull or create the simulation containers.

## Development setup

You need:

   * Python 3
   * Python PIP (`$ sudo apt-get install python3-pip`)
   * RabbitMQ (`$ sudo apt-get install rabbitmq-server`)
   * for matplotlib libfreetype and libpng (`$ sudo apt-get install libfreetype6-dev libpng12-dev`)
   * postgres (`$ sudo apt-get install postgresql postgresql-server-dev-all`)


Now to install the required libraries run inside the rodrigues folder:

    $ sudo pip3 install -r requirements.txt


First you need to inform Django that you want to use the development settings:

    $ export DJANGO_SETTINGS_MODULE=rodrigues.settings.development


Now you are ready to start the pipeline. To start the django server you first
need to populate the database:

    $ python3 ./manage.py migrate

and create a superuser:

    $ python3 ./manage.py createsuperuser

Now you can run a development webserver using:

    $ python3 ./manage.py runserver


To run the scheduled simulations you need to run a broker and celery worker:

    $ make broker &
    $ make worker &

