import pytest

from dataland.storage import Storage, dataset_template
from dataland.utils import timestamp

def test_dataset_template_returns_empty_dataframe_matching_file():
    assert True

class TestStorage(object):

    @pytest.fixture
    def storage(self):
        s = Storage()
        s.local_dir = 'tmp/{}'.format(timestamp())
        return s

    def test_local_path_raises_if_relative_path_specified(self, storage):
        with pytest.raises(ValueError):
            storage.local_path('../relative/../path.csv')

    def test_local_path_returns_abosolute_path_to_cache_directory(self, storage):
        assert storage.local_path('absolute/path.csv') == "{}/absolute/path.csv".format(storage.local_dir)
