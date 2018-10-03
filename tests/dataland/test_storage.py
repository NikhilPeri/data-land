import pytest

from dataland.storage import Storage, timestamp

@pytest.fixture
def storage():
    s = Storage()
    s.local_dir = 'tmp/{}'.format(timestamp())
    return s

def test_local_path_raises_if_relative_path_specified(storage):
    with pytest.raises(ValueError):
        storage.local_path('../relative/../path.csv')

def test_local_path_returns_abosolute_path_to_cache_directory(storage):
    assert storage.local_path('absolute/path.csv') == "{}/absolute/path.csv".format(storage.local_dir)

def test_remote_path_raises_if_relative_path_specified(storage):
    with pytest.raises(ValueError):
        storage.remote_path('../relative/../path.csv')

def test_remote_path_returns_abosolute_path_to_gcloud_bucket(storage):
    assert storage.remote_path('absolute/path.csv') == "gs://{}/absolute/path.csv".format(storage.bucket.name)
