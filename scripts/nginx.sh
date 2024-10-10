#!/bin/bash
set -e

echo Running gen_nginx_conf...
python3 /src/scripts/gen_nginx_conf.py /etc/nginx/conf.d/nitter.conf /etc/nginx/.htpasswd

echo Launching nginx...
nginx
