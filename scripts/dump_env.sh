#!/bin/bash
set -e

echo Dumping env...
echo TWITTER_USERNAME=$TWITTER_USERNAME > /src/.env
echo TWITTER_PASSWORD=$TWITTER_PASSWORD >> /src/.env
