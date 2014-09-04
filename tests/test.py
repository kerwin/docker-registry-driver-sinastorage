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
            'sinastorage_bucket': 'test',
            'sinastorage_accesskey': 'yc0lnn31dUB6okXEEdGZ',
            'sinastorage_secretkey': '44c161a1bc0577ddf126d1c60876ec5c8455ce90'
        })
        print '&' * 100
        print self.config.sinastorage_accesskey
        print self.config.sinastorage_secretkey
        print '&' * 100
        print '&' * 100

    def setUp(self):
        super(TestDriver, self).setUp()
        self._storage._swift_connection.put_container(
            self._storage._swift_container
        )

    def tearDown(self):
        super(TestDriver, self).tearDown()
        self._storage._swift_connection.delete_container(
            self._storage._swift_container
        )

    def test_remove_inexistent(self):
        pass

    def test_list_directory(self):
        # Test with root directory
        super(TestDriver, self).test_list_directory()
        self.tearDown()

        # Test with custom root directory
        self.config = testing.Config({'storage_path': '/foo'})
        self.setUp()
        super(TestDriver, self).test_list_directory()

    def test_swift_root_path_default(self):
        assert self._storage._root_path == '/'
        assert self._storage._init_path() == ''
        assert self._storage._init_path('foo') == 'foo'

    def test_swift_root_path_empty(self):
        config = testing.Config({'storage_path': ''})
        self._storage.__init__(config=config)
        assert self._storage._init_path() == ''
        assert self._storage._init_path('foo') == 'foo'

    def test_swift_root_path_custom(self):
        config = testing.Config({'storage_path': '/foo'})
        self._storage.__init__(config=config)
        assert self._storage._init_path() == 'foo'
        assert self._storage._init_path('foo') == 'foo/foo'
