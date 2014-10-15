Django based simulation schedular
=================================

Installation
------------

Install Docker:

    * https://docs.docker.com/installation/

install fig:

    * http://www.fig.sh/install.html

checkout the git repo:

    * $ git clone https://github.com/ska-sa/ceiling-kat
    * $ cd ceiling-kat/surf\_kat

open fig.yml and under django, environment set:

    * SECRET\_KEY
    * HOSTNAME

and then run:
    * $ fig up
    * $ fig run django python django-manage syncdb

And answer the questions. Yes, you want to create a superuser.

This will start a webserver on port 80.

