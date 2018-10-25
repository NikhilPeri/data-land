import pytest
import pandas as pd
from tests.utils import Template, as_dicts

@pytest.fixture
def data_dicts():
    return [
        {'id': 1, 'value': 'A'},
        {'id': 2, 'value': 'B'},
    ]

@pytest.fixture
def data_dataframe():
    return pd.DataFrame([
        {'id': 1, 'value': 'A'},
        {'id': 2, 'value': 'B'},
    ])

@pytest.fixture
def data_template():
    return Template({
        'id':     1,
        'value': 'A',
    })

def test_as_dicts_converts_dataframe_to_dicts(data_dicts, data_dataframe):
    assert as_dicts(data_dataframe) == data_dicts

def test_template_as_dataframe_makes_dataframe_with_default_values(data_template):
    dataframe = data_template.as_dataframe([
        {},
        {'id': 2},
        {'id': 3, 'value': 'B'}
    ])
    assert as_dicts(dataframe) == sorted([
        {'id': 1, 'value': 'A'},
        {'id': 2, 'value': 'A'},
        {'id': 3, 'value': 'B'},
    ])

def test_template_as_dicts_makes_dicts_with_default_values(data_template):
    dicts = data_template.as_dicts([
        {},
        {'id': 2},
        {'id': 3, 'value': 'B'}
    ])
    assert sorted(dicts) == sorted([
        {'id': 1, 'value': 'A'},
        {'id': 2, 'value': 'A'},
        {'id': 3, 'value': 'B'},
    ])
