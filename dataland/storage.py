import os
import re
import hashlib
import base64
import pandas as pd

from dataland import config
from dataland.utils import timestamp
from google.cloud import storage as gcloud_storage

def validate_path(path):
    if path.find('..') is not -1:
        raise ValueError('illegal relative path "{}"'.format(path))
    return path

def latest_path(path, type=''):
    paths = [p for p in os.listdir(path) if p.endswith(type) ]
    return os.path.join(path, sorted(paths)[-1])

def file_hash(filepath):
    with open(filepath, mode='r') as file:
        return base64.b64encode(hashlib.md5(file.read()).digest())

def dataset_template(dataset_path):
    return pd.DataFrame(columns=pd.read_csv(dataset_path, nrows=1).columns)

class StorageContext(object):
    def __init__(self, _storage, filepath, mode):
        self.storage = _storage
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
        self.bucket = gcloud_storage.Client().bucket(config['storage']['gcloud_bucket'])
        self.local_dir = os.path.join(os.getcwd(), 'tmp/cache')

    def open(self, filepath, mode='r'):
        return StorageContext(self, filepath, mode)

    def pull(self, path):
        for blob in self.list_blobs(path):
            local_path = self.local_path(blob.name)
            try:
                if file_hash(local_path) != blob.md5_hash:
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
            parent_dir = re.sub(r'{}[/]'.format(self.local_dir), '', parent_dir)
            for file in files:
                filename = os.path.join(parent_dir, file)
                blob = self.bucket.blob(filename)
                if file_hash(self.local_path(filename)) != blob.md5_hash:
                    blob.upload_from_filename(self.local_path(filename))

    def list(self, path):
        blobs = list(self.list_blobs(path))
        return { re.search('{}/[^/]+'.format(path), b.name).group() for b in blobs }

    def list_blobs(self, path=''):
        return self.bucket.list_blobs(prefix=path)

    def local_path(self, path):
        return os.path.join(self.local_dir, validate_path(path))

storage = Storage()
