FROM ubuntu:14.04
MAINTAINER gijs@pythonic.nl
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ADD docker/apt.sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python3-numpy python3-pip python3-psycopg2 python3-matplotlib
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
RUN python3 ./manage.py collectstatic --noinput
