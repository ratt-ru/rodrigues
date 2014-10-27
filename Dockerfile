FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time
ADD docker/casarc /root/.casarc
ADD . /code
WORKDIR /code
VOLUME /results

