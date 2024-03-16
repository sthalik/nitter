#!/bin/bash
set -e

echo Running auth...
python /src/scripts/auth.py /nitter-data/guest_accounts.json

echo Generating nitter conf...
python /src/scripts/gen_nitter_conf.py /src/nitter.conf

echo Waiting for redis...
counter=0
while ! redis-cli ping; do
    sleep 1
    counter=$((counter+1))
    if [ $counter -ge 30 ]; then
        echo "Redis was not ready after 30 seconds, exiting"
        exit 1
    fi
done

echo Launching nitter...
/src/nitter
