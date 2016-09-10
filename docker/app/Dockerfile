FROM alpine:3.4

RUN mkdir /var/app \
 && echo "@edge http://nl.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
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
            openssl \
            openssl-dev \
            pcre-dev \
            postgresql-dev \
            python2@edge \
            python2-dev@edge \
            py2-pip@edge \
 && npm install -g gulp

COPY ["start.sh", "set_host.sh", "cert.crt", "cert.key", "/var/app/"]

EXPOSE 8080

CMD ["bash", "/var/app/start.sh"]

