# Docker registry sinastorage driver

This is a [docker-registry backend driver][registry-core] for [Sina Cloud Storage][sina-cloud-storage].

## Usage (recommendation)

Go to [Sina Cloud Storage][sina-cloud-storage] to get your access_key first.

Run docker-registry service by docker container

```
docker run --rm \
  -e SETTINGS_FLAVOR=sinastorage \
  -e SINASTORAGE_BUCKET=YOUR_BUCKET \
  -e SINASTORAGE_ACCESSKEY=YOUR_ACCESSKEY \
  -e SINASTORAGE_SECRETKEY=YOUR_SECRETKEY \
  -p 5000:5000 \
  --name registry \
  kerwin/docker-registry-sinastorage
```

## Usage via pip

```
# Install pip
apt-get -y install python-pip

# Install deps for backports.lzma (python2 requires it)
apt-get -y install python-dev liblzma-dev libevent1-dev

# Install docker-registry
pip install docker-registry

# finally
pip install docker-registry-driver-sinastorage

export DOCKER_REGISTRY_CONFIG=/usr/local/lib/python2.7/dist-packages/config/config_sinastorage.yml
export SETTINGS_FLAVOR=sinastorage

export SINASTORAGE_BUCKET=YOUR_BUCKET
export SINASTORAGE_ACCESSKEY=YOUR_ACCESSKEY
export SINASTORAGE_SECRETKEY=YOUR_SECRETKEY
docker-registry
```

## Contributing

In order to verify what you did is ok, just run `pip install tox; tox`. This will run the tests
provided by [`docker-registry-core`][registry-core].

For more information, plz check [`docker-registry-readme`][registry-readme]

[pypi-url]: https://pypi.python.org/pypi/docker-registry-driver-sinastorage
[registry-core]: https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core
[sina-cloud-storage]: http://open.sinastorage.com/
[registry-readme]: https://github.com/docker/docker-registry/blob/master/README.md
