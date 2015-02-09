#!make

export DJANGO_SETTINGS_MODULE=rodrigues.settings.development


.PHONY: worker broker runserver migrate makemigrations fig_migrate fig_makemigrations psql


worker:
	python3 `which celery` -A rodrigues worker -l info


broker:
	rabbitmq-server


runserver:
	python3 ./manage.py runserver


migrate:
	python3 ./manage.py migrate


migrate_sleep: 
	SECRET_KEY=bla python3 ./manage.py migrate --settings=rodrigues.settings.container
	sleep infinity


makemigrations:
	cd $(DJANGO_FOLDER) && python3 ./manage.py makemigrations


fig_migrate:
	fig run django python3 ./manage.py migrate --settings=rodrigues.settings.container


fig_makemigrations:
	fig run django python3 ./manage.py makemigrations --settings=rodrigues.settings.container


psql:
	docker run -it --link rodrigues_db_1:db1 postgres psql -h db1 -U postgres

