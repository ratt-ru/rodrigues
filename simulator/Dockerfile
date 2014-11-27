FROM gijzelaerr/papino-meqtrees
RUN apt-get install -y time git subversion policycoreutils ipython cmake
ADD casarc /root/.casarc

ADD . /code
WORKDIR /code
#RUN tar -xjvf wsclean-1.4.tar.bz2
#RUN mkdir -p /code/wsclean-1.4/build
#WORKDIR /code/wsclean-1.4/build
#RUN cmake ..
#RUN make

WORKDIR /code
RUN svn co https://svn.cv.nrao.edu/svn/casa-data/distro/geodetic
RUN git clone -b devel https://github.com/SpheMakh/pyxis
RUN tar -zxvf casapy-42.2.30986-1-64b.tar.gz
RUN mkdir /results
cmd ./runsim.sh
# cmd pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
