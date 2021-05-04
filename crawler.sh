#!/bin/bash
dir="$( cd "$( dirname "$0" )" && pwd )/source/json"

host="http://localhost:1985"
if [ $1 ]
then
  host=${1%/}
fi

for file in $(find $dir -name \*.json ! -name 'default.json')
do
  base=$(echo $dir | sed 's/\//\\\//g')
  path=$(echo $file | sed -e "s/\.json//g;s/$base//g;s/index\.html//g")
  url="$host$path"

  echo $(curl -s -o /dev/null -w "%{http_code} %{time_total} $url" "$url")
done
