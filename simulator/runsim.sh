#!/bin/bash
setsebool -P allow_execheap=1
export PATH=/code/pyxis/Pyxis/bin:/code/casapy-42.2.30986-1-64b/bin:/code/wsclean/wsclean/build:/code/PyMORESANE/bin:$PATH
export PYTHONPATH=/code/pyxis:$PYTHONPATH
if [ -z "$USER"]; then
  export USER=root
fi
pyxis -s /code/src -s . CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
