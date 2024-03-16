FROM alpine:3.18 as nim
LABEL maintainer="setenforce@protonmail.com"

RUN apk --no-cache add libsass-dev pcre gcc git libc-dev "nim=1.6.14-r0" "nimble=0.13.1-r2"

WORKDIR /src/nitter

COPY nitter.nimble .
RUN nimble install -y --depsOnly

COPY . .
RUN nimble build -d:danger -d:lto -d:strip \
    && nimble scss \
    && nimble md

FROM alpine:3.18 as overmind
RUN apk --no-cache add go
RUN go install github.com/DarthSim/overmind/v2@latest

FROM alpine:3.18
WORKDIR /src/
# RUN apk --no-cache add pcre ca-certificates openssl1.1-compat
RUN apk --no-cache add pcre ca-certificates openssl1.1-compat bash redis tmux nginx python3 py3-pip
RUN pip install requests
COPY --from=nim /src/nitter/nitter ./
# COPY --from=nim /src/nitter/nitter.example.conf ./nitter.conf
COPY --from=nim /src/nitter/public ./public
COPY --from=overmind /root/go/bin/overmind ./
COPY Procfile ./Procfile
COPY scripts/assets/redis.conf ./redis.conf
COPY fly.nitter.conf ./nitter.conf
COPY scripts/ ./scripts/
COPY fly.nginx.conf /etc/nginx/nginx.conf
COPY fly.nginx-site.conf /etc/nginx/conf.d/nitter.conf
COPY .htpasswd /etc/nginx/.htpasswd
# Assumes /nitter-data is already volume mounted from docker or PaaS
RUN mkdir -p /nitter-data/redis
EXPOSE 8080
# RUN adduser -h /src/ -D -s /bin/sh nitter
# USER nitter
CMD ["bash", "-c", "/src/scripts/dump_env.sh && /src/overmind s"]
