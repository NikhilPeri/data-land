import pytest

import os
import pandas as pd
from dataland.dataset import IncrementalDataset

@pytest.fixture
def dataset():
    return pd.DataFrame({'col_a': [1, 2, 3], 'col_b': [4, 5, 6]})

class TestIncrementalDataset(object):
    def test_creates_new_local_dataset(self):
        incremental = IncrementalDataset('tmp/sample_dataset')
        metadata = open('tmp/sample_dataset/.metadata')

        assert metadata.read() == '{"first_drop": null, "drop_count": 0, "last_drop": null, columns: []}'

    @pytest.mark.freeze_time('2018-04-20 16:20:00.012')
    def test_store_create_new_data_drop(self, dataset):
        incremental = IncrementalDataset('tmp/sample_dataset/')

        assert not os.path.isfile('tmp/sample_dataset/2018-04-20-1620.csv')
        incremental.store(dataset)

        assert os.path.isfile('tmp/sample_dataset/2018-04-20-1620.csv')
