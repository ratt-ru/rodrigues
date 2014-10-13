#!make

export DJANGO_SETTINGS_MODULE=surf_kat.settings.development

.PHONY: all worker

all: worker

worker:
	celery -A surf_kat worker -l info

amqp:
	rabbitmq-server

django:
	./manage.py runserver

syncdb:
	./manage.py --settings=surf_kat.settings.development syncdb

