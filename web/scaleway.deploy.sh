#!/bin/bash

cp -r scaleway scaleway.tmp
find scaleway.tmp/* -type f \( -iname '*.html' -or -iname '*.js' -or -iname '*.css' \) -exec gzip "{}" \; -exec mv "{}.gz" "{}" \;
aws s3 rm s3://scaleway.magentix.fr  --recursive
aws s3 cp scaleway.tmp s3://scaleway.magentix.fr --recursive --exclude "*.html" --exclude "*.css" --exclude "*.js"
aws s3 cp scaleway.tmp s3://scaleway.magentix.fr --recursive --exclude "*" --include '*.html' --content-encoding gzip --cache-control "max-age=3600" --content-type 'text/html; charset=UTF-8'
aws s3 cp scaleway.tmp s3://scaleway.magentix.fr --recursive --exclude "*" --include '*.css' --content-encoding gzip --cache-control "max-age=3600" --content-type 'text/css; charset=UTF-8'
aws s3 cp scaleway.tmp s3://scaleway.magentix.fr --recursive --exclude "*" --include '*.js' --content-encoding gzip --cache-control "max-age=3600" --content-type 'application/javascript; charset=UTF-8'
rm -rf scaleway.tmp
