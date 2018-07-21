import pytest

from dataland.file_utils import incremental_timestamp

@pytest.mark.freeze_time('2018-04-20 16:20:00.012')
def test_incremental_timestamp():
    assert incremental_timestamp() == '2018-04-20-1620'
