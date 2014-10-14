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

fig:
	fig up

fig_syncdb:
	fig run django ./manage.py syncdb

fig_restart:
	fig stop && fig rm --force && fig build && fig up -d
