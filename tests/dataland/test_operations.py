import pytest
from mock import call
import pandas as pd

from tests.utils import as_dicts, Template, MockStorageTestCase

from dataland.operations import AppendOperation, TransformOperation
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
        ]).reindex(columns=['value', 'id'])
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

class DummyJoinTransformOperation(TransformOperation):
    INPUTS={
        'dataframe_one': 'transform_operation_dataframe_one.csv',
        'dataframe_two': 'transform_operation_dataframe_two.csv'
    }
    OUTPUT='transform_operation_output.csv'

    def transform(self, dataframe_one, dataframe_two):
        return (
            pd.merge(dataframe_one, dataframe_two, how='inner', on='id')
              .rename(columns={'value_x': 'value_one', 'value_y': 'value_two'})
        )

class TestTransformOperation(MockStorageTestCase):

    def setUp(self):
        super(TestTransformOperation, self).setUp()
        dataframe_one = template.as_dataframe([
            {},
            {'id': 2, 'value': 'B'}
        ])
        self.store_dataframe(dataframe_one, DummyJoinTransformOperation.INPUTS['dataframe_one'])
        dataframe_two = template.as_dataframe([
            {'value': 'AA'},
            {'id':2, 'value': 'BB'}
        ])
        self.store_dataframe(dataframe_two, DummyJoinTransformOperation.INPUTS['dataframe_two'])

    def test_pulls_input_dataset(self):
        operation = DummyJoinTransformOperation()
        operation.perform()

        assert sorted(storage.pull.call_args_list) == sorted([
            call(operation.INPUTS['dataframe_one']),
            call(operation.INPUTS['dataframe_two'])
        ])

    def test_writes_transformed_dataframe_to_output(self):
        transformed = pd.DataFrame([
            {'id': 1, 'value_one': 'A', 'value_two': 'AA'},
            {'id': 2, 'value_one': 'B', 'value_two': 'BB'}
        ])

        operation = DummyJoinTransformOperation()
        operation.perform()

        assert as_dicts(self.retrieve_dataframe(DummyJoinTransformOperation.OUTPUT)) == as_dicts(transformed)

    def test_pushes_output_dataset(self):
        operation = DummyJoinTransformOperation()
        operation.perform()

        storage.push.assert_called_once_with(operation.OUTPUT)
