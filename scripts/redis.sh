#!/bin/bash
set -e

echo Checking if /nitter-data mount exists...
if [ ! -d "/nitter-data" ]; then
  echo "/nitter-data does not exist"
  exit 1
fi

echo Creating redis data dir just in case...
mkdir -p /nitter-data/redis

echo Launching redis...
redis-server /src/redis.conf
