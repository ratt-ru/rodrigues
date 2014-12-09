FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time git subversion policycoreutils cmake
ADD casarc /root/.casarc

ADD . /code
WORKDIR /code
RUN apt-get build-dep -y wsclean 
RUN git clone http://git.code.sf.net/p/wsclean/code wsclean
RUN mkdir -p /code/wsclean/wsclean/build
WORKDIR /code/wsclean/wsclean/build
RUN cmake ..
RUN make -j 8

WORKDIR /code
RUN svn co https://svn.cv.nrao.edu/svn/casa-data/distro/geodetic
RUN git clone -b devel https://github.com/SpheMakh/pyxis
RUN tar -zxvf casapy-42.2.30986-1-64b.tar.gz
RUN mkdir /results
cmd ./runsim.sh
# cmd pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
