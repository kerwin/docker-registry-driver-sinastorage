from docker_registry.contrib import sinastorage
from docker_registry.contrib.sinastorage import SCSBucket, KeyNotFound

from docker_registry.core import driver
from docker_registry.core import exceptions
from docker_registry.core import lru
import StringIO
import tempfile
import os

class Storage(driver.Base):

    def __init__(self, path=None, config=None):
        sinastorage.setDefaultAppInfo(config.sinastorage_accesskey, config.sinastorage_secretkey)

        self._bucket_name = config.sinastorage_bucket
        self._bucket = SCSBucket(config.sinastorage_bucket, secure=False)

        all_buckets = SCSBucket().list_buckets()
        if config.sinastorage_bucket not in [bucket for bucket, t in all_buckets]:
            self._bucket.put_bucket()

    def _init_path(self, path=None):
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

        output = StringIO.StringIO()
        try:
            for buf in self.get_store(path, self.buffer_size):
                output.write(buf)
            return output.getvalue()
        finally:
            output.close()

    def get_store(self, path, chunk_size=None):
        try:
            response = self._bucket[path]
        except KeyNotFound:
            raise exceptions.FileNotFoundError('%s is not there' % path)

        try:
            while True:
                chunk = response.read(chunk_size)
                if not chunk: break
                yield chunk
        except:
            raise IOError("Could not get content: %s" % path)

    @lru.set
    def put_content(self, path, content):
        path = self._init_path(path)
        self.put_store(path, content)
        return path

    def put_store(self, path, content, chunk=None, length=None):
        headers = {}
        if length is not None:
            headers['Content-Length'] = str(length)

        try:
            self._bucket.put(path, content, headers=headers)
        except Exception:
            raise IOError("Could not put content: %s" % path)

    def stream_read(self, path, bytes_range=None):
        path = self._init_path(path)
        for buf in self.get_store(path, self.buffer_size):
            yield buf

    def stream_write(self, path, fp):
        path = self._init_path(path)

        if hasattr(fp, '__len__'):
            length = len(fp)
            self.put_store(path, fp, chunk=self.buffer_size, length=length)
        else:
            tmp_file = tempfile.mktemp()
            try:
                with open(tmp_file, 'w') as f:
                    while True:
                        buf = fp.read(self.buffer_size)
                        if not buf: break
                        f.write(buf)

                with open(tmp_file, 'r') as f:
                    self.put_store(path, f, chunk=self.buffer_size)
            except:
                raise
            finally:
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)

    def head_store(self, path):
        obj = self._bucket.info(path)
        return obj

    def list_directory(self, path=None):
        try:
            path = self._init_path(path)
            if path and not path.endswith('/'):
                path += '/'
            files_generator = self._bucket.listdir(prefix=path)
            if len(list(files_generator)) == 0:
                raise Exception('empty')
            files_generator = self._bucket.listdir(prefix=path)
            for item in files_generator:
                yield item[0]
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

        is_dir = False
        for item in self._bucket.listdir(prefix=path+'/'):
            self._bucket.delete(item[0])
            is_dir = True

        if not is_dir:
            try:
                self._bucket.info(path)
            except Exception:
                raise exceptions.FileNotFoundError('%s is not there' % path)

        self._bucket.delete(path)

    def get_size(self, path):
        path = self._init_path(path)
        try:
            headers = self.head_store(path)
            return headers['size']
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)
