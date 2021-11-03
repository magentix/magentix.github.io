#!/bin/bash
dir="$( cd "$( dirname "$0" )" && pwd )"

python3 "$dir/tools/crawler.py" full
python3 "$dir/tools/sitemap.py"
git add -A "$dir/docs"
git commit -m "New website release"
git push