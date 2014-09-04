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
            'sinastorage_accesskey': 'yc0lnn31dUB6okXEEdGZ',
            'sinastorage_secretkey': '44c161a1bc0577ddf126d1c60876ec5c8455ce90'
        })


