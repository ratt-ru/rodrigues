INSTANCE_NAME=ceiling-kat
ZONE=europe-west1-a
IMAGE=container-vm-v20140929
MACHINE_TYPE=f1-micro

.PHONY: all delete ssh

all: ssh

create:
	gcloud compute instances create $(INSTANCE_NAME) \
		--image ${IMAGE} \
		--image-project google-containers \
		--zone $(ZONE) \
		--machine-type ${MACHINE_TYPE}
	touch create

delete:
	gcloud compute instances delete --zone $(ZONE) $(INSTANCE_NAME) 
	rm -f create

ssh: create
	gcloud compute ssh --zone $(ZONE) $(INSTANCE_NAME)

ip:
	@gcloud compute instances describe ceiling-kat --zone europe-west1-a | grep natIP | awk '{ print $$2 }'
