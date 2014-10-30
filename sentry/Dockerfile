FROM ubuntu:14.04
MAINTAINER gijs@pythonic.nl
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    python-pip \
    postgresql-client-common \
    libpq-dev \
    mysql-client \
    libmysqlclient-dev

RUN pip install MySQL-python psycopg2 sentry redis>="2.7.0,<2.9.0"

EXPOSE 9000
ONBUILD ADD sentry.conf.py /sentry.conf.py

CMD /usr/local/bin/sentry --config=/sentry.conf.py start
