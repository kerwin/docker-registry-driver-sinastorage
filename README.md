# Docker registry sinastorage driver

This is a [docker-registry backend driver][registry-core] for
[Sina Cloud Storage](http://open.sinastorage.com/).

## Usage

Assuming you have a working docker-registry setup:

```
pip install docker-registry-driver-sinastorage
```

Then edit your docker-registry configuration so that `storage` reads `sinastorage`.

## Options

You may add any of the following to your main docker-registry configuration to further configure it:

```yaml
storage: sinastorage
storage_path: /registry
sinastorage_bucket: _env:SINASTORAGE_BUCKET
sinastorage_accesskey: _env:SINASTORAGE_ACCESSKEY
sinastorage_secretkey: _env:SINASTORAGE_SECRETKEY
```

## Contributing

In order to verify what you did is ok, just run `pip install tox; tox`. This will run the tests
provided by [`docker-registry-core`][registry-core].

[pypi-url]: https://pypi.python.org/pypi/docker-registry-driver-sinastorage
[registry-core]: https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core

