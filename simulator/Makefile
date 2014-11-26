#!make
IMAGE_NAME=gijzelaerr/simulator

.PHONY: all build run force-build

all: build

build:
	docker build -t $(IMAGE_NAME) .

force-build:
	docker build -t $(IMAGE_NAME) --no-cache=true .

run:
#	docker run -v `pwd`:/results $(IMAGE_NAME) pyxis CFG=webkat_default.cfg azishe OUTDIR=/results
	docker run -v `pwd`:/results $(IMAGE_NAME) ./runsim.sh
	
	