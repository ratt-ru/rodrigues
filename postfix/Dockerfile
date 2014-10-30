FROM ubuntu:14.04
MAINTAINER gijs@pythonic.nl
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN echo "postfix postfix/main_mailer_type string Internet site" > preseed.txt
RUN echo "postfix postfix/mailname string ceiling-kat.meqtrees.net" >> preseed.txt
RUN debconf-set-selections preseed.txt
RUN DEBIAN_FRONTEND=noninteractive apt-get install -q -y postfix mailutils

RUN postconf -e 'myhostname = ceiling-kat.meqtrees.net'
RUN postconf -e 'mydestination = localhost.localdomain, localhost'
RUN postconf -e 'mynetworks = 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16'
RUN postconf -e 'smtp_dns_support_level = enabled'
RUN postconf -e 'inet_protocols = ipv4'

RUN echo "root: gijsmolenaar@gmail.com" >> /etc/aliases
RUN newaliases

EXPOSE 25

VOLUME /var/lib/postfix /var/log /var/spool/postfix

CMD service rsyslog start && service postfix start && sleep 2 &&  tail -f /var/log/mail.log
