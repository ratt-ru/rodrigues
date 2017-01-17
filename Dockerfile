FROM ubuntu:16.04
MAINTAINER gijs@pythonic.nl
ENV PYTHONUNBUFFERED 1

# allow the worker to run as root
ENV C_FORCE_ROOT true

# libc6-dev is for uwsgi
RUN apt-get update && apt-get install -qy --no-install-recommends \
		python3-pip \
        python3-psycopg2 \
        gcc \
        libc6-dev \ 
        libpython3-dev \
	    && rm -rf /var/lib/apt/lists/*

# nginx connection
RUN mkdir /socket

## mount the django code here
RUN mkdir /code

# fix broker pip
RUN pip3 install --upgrade pip setuptools

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /code

CMD ./manage.py runserver
