FROM ubuntu:14.04
MAINTAINER gijs@pythonic.nl
ENV PYTHONUNBUFFERED 1

# allow the worker to run as root
ENV C_FORCE_ROOT true

RUN apt-get update && apt-get install -qy --no-install-recommends \
		python3-numpy \
		python3-pip \
		python3-psycopg2 \
		python3-matplotlib \
		libc6-dev \
		git \
        gcc \
        libpython3-dev \
	    && rm -rf /var/lib/apt/lists/*

# nginx connection
RUN mkdir /socket

## mount the django code here
RUN mkdir /code

# fix broker pip
RUN pip3 install --upgrade pip

ADD requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /code

CMD ./manage.py runserver
