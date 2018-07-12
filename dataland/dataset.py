import os
import json
import pandas as pd

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
        


    def _new(self):
        os.makedirs(self.directory)
        with open(self._metadata_path,  'w+') as metadata:
            NEW_METADATA = { 'drop_count': 0, 'first_drop': None, 'last_drop': None }
            metadata.write(json.dumps(NEW_METADATA))
            self.metadata = NEW_METADATA
