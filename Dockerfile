# VERSION 0.1

# Latest Ubuntu LTS
from ubuntu:14.04
maintainer Kerwin Piao <piaoyuankui@gmail.com>

# Update
run apt-get update
run apt-get -y upgrade

# Install pip
run apt-get -y install python-pip

# Install deps for backports.lzma (python2 requires it)
run apt-get -y install python-dev liblzma-dev libevent1-dev

# Install docker-registry
run pip install docker-registry docker-registry-driver-sinastorage

add . /docker-registry-driver-sinastorage

env DOCKER_REGISTRY_CONFIG /docker-registry-driver-sinastorage/config/config_sinastorage.yml
env SETTINGS_FLAVOR sinastorage

expose 5000

cmd exec docker-registry
