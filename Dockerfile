FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y git time
ADD docker/casarc /root/.casarc
ADD . /opt/ceiling-kat
WORKDIR /opt/ceiling-kat
VOLUME /results

