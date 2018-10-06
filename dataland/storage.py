import os
import re
import hashlib
import base64

from dataland import config
from dataland.utils import timestamp
from google.cloud import storage

def validate_path(path):
    if path.find('..') is not -1:
        raise ValueError('illegal relative path "{}"'.format(path))
    return path

class StorageContext(object):
     def __init__(self, storage, filepath, mode):
         self.storage = storage
         self.filepath = filepath
         self.mode = mode

    def __enter__(self):
        self.storage.pull(filepath)
        self.file = open(self.storage.local_path(filepath), mode=self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_value is None and re.match(r'[wa]', self.mode) is not None:
            self.file.close()
            self.storage.push(filepath)
        return True

class Storage(object):
    def __init__(self):
        if not os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS'):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['storage']['gcloud_credentials']
        self.bucket = storage.Client().bucket(config['storage']['gcloud_bucket'])
        self.local_dir = validate_path(config['storage']['local_dir'])
        self.local_dir += '/' if not self.local_dir.endswith('/') else ''

    def open(self, filepath, mode='r'):
        return StorageContext(self, filepath, mode)

    def pull(self, path):
        for blob in self.list_blobs(path):
            local_path = self.local_path(blob.name)
            try:
                with open(local_path, mode='r') as file:
                    hash = base64.b64encode(hashlib.md5(file.read()).digest())
                    if hash != blob.md5_hash:
                        raise Exception('local cache invalid')
            except:
                try:
                    os.makedirs(os.path.dirname(local_path))
                except OSError as e:
                    pass
                blob.download_to_filename(local_path)

    def push(self, path):
        local_path = self.local_path(path)

        if os.path.isfile(local_path):
            self.bucket.blob(path).upload_from_filename(local_path)
            return

        for parent_dir, _, files in os.walk(local_path):
            parent_dir = parent_dir.replace(self.local_dir, '')
            for file in files:
                filename = os.path.join(parent_dir, file)
                import pdb; pdb.set_trace()
                blob = self.bucket.blob(filename)
                blob.upload_from_filename(self.local_path(filename))

    def list(self, path):
        blobs = list(self.list_blobs(path))
        return { re.search('{}/[^/]+'.format(path), b.name).group() for b in blobs }

    def list_blobs(self, path=''):
        return self.bucket.list_blobs(prefix=path)

    def local_path(self, path):
        return os.path.join(self.local_dir, validate_path(path))
