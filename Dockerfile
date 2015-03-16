FROM ubuntu:14.04
MAINTAINER gijs@pythonic.nl
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# allow the worker to run as root
ENV C_FORCE_ROOT true

RUN apt-get update
RUN apt-get install -y python3-numpy python3-pip python3-psycopg2 python3-matplotlib libc6-dev

RUN mkdir /socket
VOLUME /socket

## mount the django code here
RUN mkdir /code
WORKDIR /code

# required to fetch aplpy from github
RUN apt-get install -yq git

# fix broker pip
RUN easy_install3 -U pip

ADD requirements.txt /
RUN pip install -r /requirements.txt
