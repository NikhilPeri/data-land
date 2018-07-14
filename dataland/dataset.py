import os
import json
import numpy as np
import pandas as pd
from datetime import datetime

def incremental_timestamp():
    return datetime.utcnow().strftime('%Y-%m-%d-%H%M')

class IncrementalDataset(object):
    def __init__(self, directory):
        self.directory = directory
        self._metadata_path = os.path.join(self.directory, '.metadata')

        if os.path.exists(self._metadata_path):
            with open(self._metadata_path,  'r') as metadata:
                self.metadata = json.load(metadata)
        else:
            self._new()

    def load(self, start=None, end=None):
        data_drops = pd.Series(os.listdir(self.directory))

    def list_drops(self, latest=False, start=None, end=None):
        drop_files = pd.Series(os.listdir(self.directory))
        if latest:
            return drop_files.last()

        def valid_drop(drop_filename):
            valid = drop_filename.endswith('.csv')

        return drop_files.where(valid_drop)

    def store(self, dataframe):
        if self._valid_schema(dataframe):
            dataframe.to_csv(os.path.join(self.directory, incremental_timestamp() + '.csv'))
        else:
            raise 'Invalid Schema'

    def _valid_schema(self, dataframe):
        if self.metadata['columns'] == None:
            self.metadata['columns'] = dataframe.columns.values

        return  np.array_equal(dataframe.columns.values, self.metadata['columns'])

    def _new(self, directory, columns, incremental_key):
        with open(self._metadata_path,  'w+') as metadata:
            NEW_METADATA = {
                'drop_count': 0,
                'first_drop': None,
                'last_drop': None,
                'columns': columns,
                'incremental_key': incremental_key
            }
            metadata.write(json.dumps(NEW_METADATA))
            self.metadata = NEW_METADATA
