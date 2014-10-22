#!make
IMAGE_NAME=gijzelaerr/ceiling-kat

.PHONY: all build run

all: build run

build:
	docker build -t $(IMAGE_NAME) .

force-build:
	docker build -t $(IMAGE_NAME) --no-cache=true .

run:
	docker run -v ./results:/results $(IMAGE_NAME) sh -c "cd /opt/ceiling-kat/web-kat && pyxis CFG=webkat_default.cfg azishe OUTDIR=/results"
