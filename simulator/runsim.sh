#!/bin/bash
export PATH=/code/pyxis/Pyxis/bin:$PATH
export PYTHONPATH=/code/pyxis:$PYTHONPATH
echo $PATH
echo $PYTHONPATH
which pyxis
pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe
