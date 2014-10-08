#!make

.PHONY: all build run

all: build run

build:
	docker build -t gijzelaerr/surf_kat .

force-build:
	docker build -t gijzelaerr/surf_kat  --no-cache=true .

run:
	docker run -v `pwd`/results:/results gijzelaerr/surf_kat sh -c "cd /opt/ceiling-kat/web-kat && pyxis CFG=webkat_default.cfg azishe; cp log-ska1sims.txt /results "
