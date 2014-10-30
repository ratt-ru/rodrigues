#!make
IMAGE_NAME=gijzelaerr/postfix

.PHONY: all build run force-build

all: build

build:
	docker build -t $(IMAGE_NAME) .

force-build:
	docker build -t $(IMAGE_NAME) --no-cache=true .

run:
	docker run -ti -p 25:25 $(IMAGE_NAME)
