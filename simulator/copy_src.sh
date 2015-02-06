#/usr/bin/sh
if [ -e "src" ]; then
  rm -fr src
fi
cp -r ../src .
