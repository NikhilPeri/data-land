import os

import pandas as pd

from mock import Mock
from unittest import TestCase
from tests import TEMP_DIR

from dataland.storage import storage

def as_dicts(dataframe):
    return sorted(dataframe.to_dict('records'))

class Template(object):
    def __init__(self, sample_record):
        self.sample_record = sample_record

    def as_dataframe(self, records):
        return pd.DataFrame(self.as_dicts(records))

    def as_dicts(self, records):
        dicts = []
        for record in records:
            sample = self.sample_record.copy()
            sample.update(record)
            dicts.append(sample)

        return dicts

class MockStorageTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        storage.local_dir = os.path.join(os.getcwd(), TEMP_DIR)
        os.makedirs(storage.local_dir)
        storage.pull = Mock()
        storage.push = Mock()

        super(MockStorageTestCase, self).setUp(*args, **kwargs)

    def store_dataframe(self, dataframe, path):
        dataframe.to_csv(storage.local_path(path), mode='w+', index=False)

    def retrieve_dataframe(self, dataframe_path):
        return pd.read_csv(storage.local_path(dataframe_path))
