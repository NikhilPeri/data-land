import pytest
import pandas as pd

from tests.utils import as_dicts, Template, MockStorageTestCase

from dataland.operations import AppendOperation
from dataland.storage import storage

template = Template({
    'id': 1,
    'value': 'A'
})

class DummyAppendOperation(AppendOperation):
    INPUT = 'test_append_dataset.csv'

    def __init__(self, new_records):
        self._new_records = new_records
        super(DummyAppendOperation, self).__init__()

    def new_records(self):
        return self._new_records

class TestAppendOperation(MockStorageTestCase):

    def test_append_pulls_input_dataset(self):
        self.store_dataframe(template.as_dataframe([{}]), DummyAppendOperation.INPUT)
        operation = DummyAppendOperation(template.as_dataframe([{}]))

        operation.perform()

        storage.pull.assert_called_once_with(operation.INPUT)

    def test_append_writes_new_rows_to_input(self):
        old_records = template.as_dataframe([
            {},
            {'id': 2, 'value': 'B'},
        ])
        new_records = template.as_dataframe([
            {'id': 3, 'value': 'C'},
            {'id': 4, 'value': 'D'},
        ])
        combinded_records = template.as_dataframe([
            {},
            {'id': 2, 'value': 'B'},
            {'id': 3, 'value': 'C'},
            {'id': 4, 'value': 'D'},
        ])
        self.store_dataframe(old_records, DummyAppendOperation.INPUT)
        operation = DummyAppendOperation(new_records)

        operation.perform()

        assert as_dicts(self.retrieve_dataframe(DummyAppendOperation.INPUT)) == as_dicts(combinded_records)

    def test_append_raises_if_template_does_not_match_input_template(self):
        old_records = template.as_dataframe([
            {},
            {'id': 2, 'value': 'B'},
        ])
        invalid_records = pd.DataFrame([
            {'col': 3, 'value': 'C'},
            {'col': 4, 'value': 'D'},
        ])
        self.store_dataframe(old_records, DummyAppendOperation.INPUT)
        operation = DummyAppendOperation(invalid_records)

        with pytest.raises(Exception):
            operation.perform()

        assert as_dicts(self.retrieve_dataframe(DummyAppendOperation.INPUT)) == as_dicts(old_records)

    def test_append_pushes_modified_dataset_to_storage(self):
        self.store_dataframe(template.as_dataframe([{}]), DummyAppendOperation.INPUT)
        operation = DummyAppendOperation(template.as_dataframe([{}]))

        operation.perform()

        storage.push.assert_called_once_with(operation.INPUT)
