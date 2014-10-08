#!make

.PHONY: all worker

all: worker

worker:
	celery -A surf_kat worker -l info

amqp:
	rabbitmq-server

django:
	./manage.py runserver
