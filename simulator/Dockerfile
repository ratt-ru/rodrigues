FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time
ADD casarc /root/.casarc
ADD . /code
WORKDIR /code
RUN mkdir /results
cmd pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
