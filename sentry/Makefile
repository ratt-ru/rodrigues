#!make
IMAGE_NAME=gijzelaerr/sentry

.PHONY: all build run force-build

all: build

build:
	docker build -t $(IMAGE_NAME) .

force-build:
	docker build -t $(IMAGE_NAME) --no-cache=true .

run:
	docker run -ti $(IMAGE_NAME)
