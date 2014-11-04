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

RUN apt-get install -y python-dev
RUN pip install psycopg2 sentry

EXPOSE 9000
ADD sentry.conf.py /sentry.conf.py

CMD /usr/local/bin/sentry --config=/sentry.conf.py start
