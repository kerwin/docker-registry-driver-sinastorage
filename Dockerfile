FROM registry
MAINTAINER Kerwin Piao <piaoyuankui@gmail.com>

# Add the swift support
RUN ["pip", "install", "docker-registry-driver-sinastorage"]

