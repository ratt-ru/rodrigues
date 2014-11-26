FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time
ADD casarc /root/.casarc

RUN git clone https://github.com/SpheMakh/pyxis
WORKDIR /pyxis
RUN git checkout devel
RUN export PATH=./pyxis/Pyxis/bin:$PATH
RUN export PYTHONPATH=./pyxis:$PYTHONPATH

ADD . /code
WORKDIR /code
RUN mkdir /results
cmd pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
