Django based simulation schedular
=================================

Installation
------------

install python libraries:

    $ pip install -r requirements

install:

 * rabbitmq


run all in seperate terminals:

 $ make syncdb
 $ make amqp
 $ make worker
 $ make django
