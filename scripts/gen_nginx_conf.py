import sys
import os
from typing import Tuple
from passlib.apache import HtpasswdFile


RSS_PASSWORD_PLZ_CHANGE = "[RSS_PASSWORD_PLZ_CHANGE]"
HTPASSWD_FILE_PLZ_CHANGE = "[HTPASSWD_FILE_PLZ_CHANGE]"
TEMPLATE = """server {
    listen 8081;

    location ~* /rss$ {
        if ($arg_key != [RSS_PASSWORD_PLZ_CHANGE]) {
            return 200 '';
        }

        proxy_pass http://localhost:8080;
    }

    location /pic/ { proxy_pass http://localhost:8080; }
    location /video/ { proxy_pass http://localhost:8080; }

    location /css/ { proxy_pass http://localhost:8080; }

    location /js/ { proxy_pass http://localhost:8080; }
    location /fonts/ { proxy_pass http://localhost:8080; }
    location = /apple-touch-icon.png { proxy_pass http://localhost:8080; }
    location = /apple-touch-icon-precomposed.png { proxy_pass http://localhost:8080; }
    location = /android-chrome-192x192.png { proxy_pass http://localhost:8080; }
    location = /favicon-32x32.png { proxy_pass http://localhost:8080; }
    location = /favicon-16x16.png { proxy_pass http://localhost:8080; }
    location = /favicon.ico { proxy_pass http://localhost:8080; }
    location = /logo.png { proxy_pass http://localhost:8080; }
    location = /site.webmanifest { proxy_pass http://localhost:8080; }

    location / {
        auth_basic "Restricted Content";
        auth_basic_user_file [HTPASSWD_FILE_PLZ_CHANGE];

        proxy_pass http://localhost:8080;
    }
}"""

def main(rss_password: str, web_username: str, web_password: str, htpasswd_file: str) -> Tuple[str, str]:
    site_conf = TEMPLATE.replace(RSS_PASSWORD_PLZ_CHANGE, rss_password).replace(HTPASSWD_FILE_PLZ_CHANGE, htpasswd_file)
    ht = HtpasswdFile()
    ht.set_password(web_username, web_password)
    htpasswd = ht.to_string().decode('utf-8')

    return (site_conf, htpasswd)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 gen_nginx_conf.py <site_conf_file> <htpasswd_file>")
        sys.exit(1)

    site_conf_file = sys.argv[1]
    htpasswd_file = sys.argv[2]

    rss_password = os.getenv("INSTANCE_RSS_PASSWORD")
    if not rss_password:
        print("Please set environment variable INSTANCE_RSS_PASSWORD")
        sys.exit(1)
    web_username = os.getenv("INSTANCE_WEB_USERNAME")
    if not web_username:
        print("Please set environment variable INSTANCE_WEB_USERNAME")
        sys.exit(1)
    web_password = os.getenv("INSTANCE_WEB_PASSWORD")
    if not web_password:
        print("Please set environment variable INSTANCE_WEB_PASSWORD")
        sys.exit(1)

    (site_conf, htpasswd) = main(rss_password, web_username, web_password, htpasswd_file)

    with open(site_conf_file, "w") as f:
        f.write(site_conf)
    with open(htpasswd_file, "w") as f:
        f.write(htpasswd)
