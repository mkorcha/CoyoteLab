FROM alpine:3.6

RUN mkdir /var/app \
 && apk update \
 && apk upgrade \
 && apk add bash \
            ca-certificates \
            gcc \
            g++ \
            libffi-dev \
            linux-headers \
            make \
            musl-dev \
            nodejs \
            nodejs-npm \
            pcre-dev \
            postgresql-dev \
            python2 \
            python2-dev \
            py2-pip \
 && npm install -g gulp

COPY ["start.sh", "set_host.sh", "cert.crt", "cert.key", "/var/app/"]

EXPOSE 8080

CMD ["bash", "/var/app/start.sh"]

