FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time git subversion
ADD casarc /root/.casarc

ADD . /code
WORKDIR /code
RUN svn co https://svn.cv.nrao.edu/svn/casa-data/distro/geodetic
RUN git clone -b devel https://github.com/SpheMakh/pyxis
RUN mkdir /results
cmd ./runsim.sh
# cmd pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
