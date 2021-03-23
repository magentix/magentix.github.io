#!/bin/bash
dir="$( cd "$( dirname "$0" )" && pwd )/build/json"

host="http://localhost:1985"
if [ $1 ]
then
  host=${1%/}
fi

for file in $(find $dir -name \*.json)
do
  base=$(echo $dir | sed 's/\//\\\//g')
  path=$(echo $file | sed -e "s/\.json//g;s/$base//g;s/index\.html//g")
  url="$host$path"

  curl -s -o /dev/null -w "%{http_code}" "$url"
  echo " $url"
done
