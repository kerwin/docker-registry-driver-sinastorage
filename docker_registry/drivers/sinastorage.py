from docker_registry.contrib import sinastorage
from docker_registry.contrib.sinastorage import SCSBucket

from docker_registry.core import driver
from docker_registry.core import exceptions
from docker_registry.core import lru


class Storage(driver.Base):

    def __init__(self, path=None, config=None):
        sinastorage.setDefaultAppInfo(config.sinastorage_accesskey, config.sinastorage_secretkey)

        self._bucket_name = config.sinastorage_bucket
        self._bucket = SCSBucket(config.sinastorage_bucket, secure=False)

        all_buckets = SCSBucket().list_buckets()
        if config.sinastorage_bucket not in [bucket for bucket, t in all_buckets]:
            self._bucket.put_bucket()
        else:
            for item in self._bucket.listdir():
                self._bucket.delete(item[0])

    def _init_path(self, path=None):
        path = self._bucket_name + path if path else self._bucket_name
        # Openstack does not like paths starting with '/'
        if path:
            if path.startswith('/'):
                path = path[1:]
            if path.endswith('/'):
                path = path[:-1]
        return path

    def content_redirect_url(self, path):
        path = self._init_path(path)
        return '/'.join([
            self._bucket.base_url,
            path
        ])

    @lru.get
    def get_content(self, path):
        path = self._init_path(path)
        return self.get_store(path)

    def get_store(self, path, chunk_size=None):
        response = self._bucket[path]
        while True:
            chunk = response.read(CHUNK)
            if not chunk: break
            yield chunk

    @lru.set
    def put_content(self, path, content):
        path = self._init_path(path)
        self.put_store(path, content)
        return path

    def put_store(self, path, content, chunk=None):
        try:
            self._bucket.put(path, content)
        except Exception:
            raise IOError("Could not put content: %s" % path)

    def stream_read(self, path, bytes_range=None):
        path = self._init_path(path)
        for buf in self.get_store(path, self.buffer_size):
            yield buf

    def stream_write(self, path, fp):
        path = self._init_path(path)
        self.put_store(path, fp, self.buffer_size)

    def head_store(self, path):
        obj = self._bucket.info(path)
        return obj

    def list_directory(self, path=None):
        try:
            path = self._init_path(path)
            if path and not path.endswith('/'):
                path += '/'
            files_generator = self._bucket.listdir()
            if not directory:
                raise
            for item in files_generator:
                print item
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    def exists(self, path):
        path = self._init_path(path)
        try:
            self.head_store(path)
            return True
        except Exception:
            return False

    @lru.remove
    def remove(self, path):
        path = self._init_path(path)
        try:
            self._swift_connection.delete_object(self._swift_container, path)
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    def get_size(self, path):
        path = self._init_path(path)
        try:
            headers = self.head_store(path)
            return headers['size']
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)
