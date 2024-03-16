#!/bin/bash
set -e

echo Dumping auth env...
echo TWITTER_USERNAME=$TWITTER_USERNAME > /src/.env
echo TWITTER_PASSWORD=$TWITTER_PASSWORD >> /src/.env
echo DEBUG=$DEBUG >> /src/.env

echo Dumping custom path env...
echo NITTER_ACCOUNTS_FILE=$NITTER_ACCOUNTS_FILE >> /src/.env

echo Dumping instance customization env...
echo FLY_APP_NAME=$FLY_APP_NAME >> /src/.env
echo INSTANCE_TITLE=$INSTANCE_TITLE >> /src/.env
echo INSTANCE_THEME=$INSTANCE_THEME >> /src/.env
echo INSTANCE_INFINITE_SCROLL=$INSTANCE_INFINITE_SCROLL >> /src/.env
