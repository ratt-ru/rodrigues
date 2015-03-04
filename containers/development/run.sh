#!/bin/bash -ve

echo
echo "** running simulation..."
echo "** sleeping for 3 seconds..."
sleep 3
echo
ls -a /input
echo
ls -a /output
echo
cat /input/parameters.json
echo 
cp -av /example_files/* /output
echo
cp -av input/parameters.json /output
echo
cp /bin/bash /output
echo
echo "done"
