FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y git time
ADD casarc /root/.casarc
RUN git clone https://github.com/ska-sa/ceiling-kat /opt/ceiling-kat
VOLUME /results

