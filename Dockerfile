FROM ubuntu
MAINTAINER Kerwin Piao <piaoyuankui@gmail.com>

# Add the swift support
RUN ["pip", "install", "docker-registry-driver-sinastorage"]


# VERSION 0.1

# Latest Ubuntu LTS
from    ubuntu:14.04

# Update
run apt-get update
run apt-get -y upgrade

# Install pip
run apt-get -y install python-pip

# Install deps for backports.lzma (python2 requires it)
run apt-get -y install python-dev liblzma-dev libevent1-dev

# Install docker-registry
run pip install docker-registry-driver-sinastorage docker-registry

env DOCKER_REGISTRY_CONFIG /docker-registry/config/config_sinastorage.yml
env SETTINGS_FLAVOR sinastorage

expose 5000

cmd exec docker-registry
