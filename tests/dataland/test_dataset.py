from dataland.dataset import IncrementalDataset

class TestIncrementalDataset(object):
    def test_creates_new_local_dataset(self):
        incremental = IncrementalDataset('tmp/sample_dataset')
        metadata = open('tmp/sample_dataset/.metadata')

        assert metadata.read() == '{"first_drop": null, "drop_count": 0, "last_drop": null}'

    def test_load_fetches_data_drops_in_span(self):
        incremental = IncrementalDataset('test/fixtures/sample_dataset')
        
