import os
from dataland import config
from datetime import datetime
from google.cloud import storage

def validate_path(path):
    if path.find('..') is not -1:
        raise ValueError('illegal relative path "{}"'.format(path))
    return path

def timestamp():
    return datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

class Storage(object):
    def __init__(self):
        if not os.environ.has_key('GOOGLE_APPLICATION_CREDENTIALS'):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['storage']['gcloud_credentials']
        self.bucket = storage.Client().bucket(config['storage']['gcloud_bucket'])
        self.local_dir = config['storage']['local_dir']

    def list(self, path):
        import pdb; pdb.set_trace()

    def fetch(self, path):
        if os.path.exists(self.local_path(path)):
            # Check MD5
            # Check remote MD5
            return True
        else:
            # Download remote
            return False

    def local_path(self, path):
        return os.path.join(self.local_dir, validate_path(path))

    def remote_path(self, path):
        return "gs://{}".format(os.path.join(self.bucket.name, validate_path(path)))
