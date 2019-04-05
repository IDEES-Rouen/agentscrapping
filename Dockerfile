############################################################
# STAGE 1
############################################################

# https://denibertovic.com/posts/handling-permissions-with-docker-volumes/
FROM python:3.6-alpine3.7 as baseStage
MAINTAINER rey <sebastien.rey-coyrehourcq@univ-rouen.fr>

RUN echo http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
RUN apk upgrade --update-cache --available
RUN apk add --update && apk add -f gnupg ca-certificates curl dpkg bash su-exec shadow gcc musl-dev libxml2-dev libxslt-dev python-dev libffi-dev openssl-dev nmap

ARG GID=1000
ARG UID=1000

ENV TZ=UTC

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN addgroup -g $GID scrapy && adduser -h /home/scrapy -s /bin/sh -D -G scrapy -u $UID scrapy

WORKDIR /home/scrapy

RUN mkdir -p /home/scrapy/backup

#COPY crontab /home/scrapy

COPY . /home/scrapy/agent
WORKDIR /home/scrapy/agent

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

VOLUME /home/scrapy/backup

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["python","main_scraping.py"]
