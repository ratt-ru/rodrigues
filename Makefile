#!make

ZONE=europe-west1-b
MACHINE_TYPE=f1-micro
INSTANCE_NAME=ceiling-kat
IMAGE=container-vm-v20141016
IMAGE_PROJECT=google-containers

DJANGO_FOLDER=django_kat

export DJANGO_SETTINGS_MODULE=django_kat.settings.development


.PHONY: all worker amqp django syncdb fig fig_syncdb fig_restart vm_create vm_delete vm_ssh vm_ip

all:

worker:
	cd $(DJANGO_FOLDER) && python3 `which celery` -A django_kat worker -l info

flower:
	cd $(DJANGO_FOLDER) && python3 `which celery` -A django_kat flower

broker:
	rabbitmq-server

django:
	cd $(DJANGO_FOLDER) && python3 ./manage.py runserver

syncdb:
	cd $(DJANGO_FOLDER) && python3 ./manage.py syncdb

migrations:
	cd $(DJANGO_FOLDER) && python3 ./manage.py makemigrations

git_pull:
	git pull

fig_up:
	fig up -d

fig_stop:
	fig stop

fig_build:
	fig build

fig_syncdb:
	fig run django python3 ./manage.py syncdb

fig_REINITIALISE:
	fig stop && fig rm --force && fig build && fig up -d

fig_reload: git_pull fig_stop fig_build fig_up fig_syncdb
	true

vm_create:
	gcloud compute instances create $(INSTANCE_NAME) \
		--image ${IMAGE} \
		--image-project $(IMAGE_PROJECT) \
		--zone $(ZONE) \
		--machine-type ${MACHINE_TYPE}

vm_delete:
	gcloud compute instances delete --zone $(ZONE) $(INSTANCE_NAME)

vm_ssh:
	gcloud compute ssh --zone $(ZONE) $(INSTANCE_NAME)

vm_ip:
	@gcloud compute instances describe $(INSTANCE_NAME) --zone $(ZONE) | grep natIP | awk '{ print $$2 }'

deploy:
	apt-get update
	apt-get install -y python-pip
	pip install fig
	fig up -d
	fig run django python3 manage.py syncdb

