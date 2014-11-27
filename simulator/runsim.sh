#!/bin/bash
setsebool -P allow_execheap=1
export PATH=/code/pyxis/Pyxis/bin:/code/casapy-42.2.30986-1-64b/bin:/code/wsclean-1.4/build:$PATH
export PYTHONPATH=/code/pyxis:$PYTHONPATH
echo $PATH
echo $PYTHONPATH
which pyxis
if [ -z "$USER"]; then
  USER=root
fi
pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
