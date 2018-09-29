from google.cloud import storage

def sanatize_path(path):
    if path.contains('..'):
        raise ValueError('relative paths "{}" not allowed'.format(path))
    else:
        return path

class BaseAdapter(object):
    def list(self, path):
        self._list(sanatize_path(path))

    def remove(self, path):
        print Hi
        pass

    def signature(self, filepath):
        raise NotImplemented


class GoogleStorageAdapter(object):
    def __init__(self):
        self.client = storage.Client()


    def list(path):
