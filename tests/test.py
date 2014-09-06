# -*- coding: utf-8 -*-

from docker_registry import testing

class TestQuery(testing.Query):
    def __init__(self):
        self.scheme = 'sinastorage'


class TestDriver(testing.Driver):
    def __init__(self):
        self.scheme = 'sinastorage'
        self.path = ''
        self.config = testing.Config({
            'sinastorage_bucket': 'test-docker-registry',
            'sinastorage_accesskey': 'PUT_YOUR_ACCESSKEY',
            'sinastorage_secretkey': 'PUT_YOUR_SECRETKEY'
        })

