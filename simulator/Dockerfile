FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time git
ADD casarc /root/.casarc

ADD . /code
WORKDIR /code
RUN git clone -b devel https://github.com/SpheMakh/pyxis
RUN mkdir /results
cmd ./runsim.sh
# cmd pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
