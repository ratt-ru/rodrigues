FROM ubuntu:14.04
MAINTAINER gijs@pythonic.nl

# Allow postfix to install without interaction.
RUN echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections
RUN echo "postfix postfix/mailname string ceiling-cat.meqtrees.net" | debconf-set-selections
RUN echo "postfix postfix/root_address string gijs@pyhonicnl" | debconf-set-selections
RUN echo "postfix postfix/mynetworks string 0.0.0.0/0" | debconf-set-selections

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install postfix

