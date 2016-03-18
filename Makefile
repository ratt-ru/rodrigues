#!make

export DJANGO_SETTINGS_MODULE=rodrigues.settings.development
export SECRET_KEY=doesntmatter


.PHONY: worker broker runserver migrate psql


# NOTE: never run the worker in autoreload mode
worker:
	python3 `which celery` -A rodrigues worker -l info


broker:
	rabbitmq-server

runserver:
	python3 ./manage.py runserver


migrate:
	python3 ./manage.py migrate

psql:
	docker run -it --link rodrigues_db_1:db1 postgres psql -h db1 -U postgres

