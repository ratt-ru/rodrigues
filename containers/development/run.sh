#!/bin/bash -ve

if [ -z "$1" ]; then
    DATA=/
else
    DATA=$1
fi


echo
echo "** running simulation..."
echo "** sleeping for 3 seconds..."
sleep 3
echo
ls -a $DATA/input
echo
ls -a $DATA/output
echo
cat $DATA/input/parameters.json
echo 
cp -av /example_files/* $DATA/output
echo
cp -av $DATA/input/parameters.json $DATA/output
echo
cp /bin/bash $DATA/output
echo
echo "done"
