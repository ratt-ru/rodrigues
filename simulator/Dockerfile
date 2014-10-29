FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time
ADD casarc /root/.casarc
ADD . /code
WORKDIR /code
RUN mkdir /results
RUN mkdir /input

