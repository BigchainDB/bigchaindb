# Main Dockerfile used to build production
# deployment image.
#
# This file is also used to build a base image
# for Dockerfile-dev to setup a dev environment

FROM python:3.6
LABEL maintainer "dev@bigchaindb.com"
RUN mkdir -p /usr/src/app
COPY . /usr/src/app/
WORKDIR /usr/src/app
RUN apt-get -qq update \
    && apt-get -y upgrade \
    && pip install --no-cache-dir . \
    && apt-get autoremove \
    && apt-get clean

ARG backend

ENV PYTHONUNBUFFERED 0
ENV BIGCHAINDB_DATABASE_PORT 27017
ENV BIGCHAINDB_SERVER_BIND 0.0.0.0:9984
ENV BIGCHAINDB_WSSERVER_HOST 0.0.0.0
ENV BIGCHAINDB_WSSERVER_SCHEME ws

ENV BIGCHAINDB_WSSERVER_ADVERTISED_HOST 0.0.0.0
ENV BIGCHAINDB_WSSERVER_ADVERTISED_SCHEME ws

ENV BIGCHAINDB_START_TENDERMINT 0
ENV TENDERMINT_PORT 46657

RUN bigchaindb -y configure "$backend"
