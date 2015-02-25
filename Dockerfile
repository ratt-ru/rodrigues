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

ADD requirements.txt /
RUN pip3 install -r /requirements.txt
