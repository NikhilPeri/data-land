import pytest
from dataland.scheduler import load_jobs

def test_all_jobs_load_sucessfully():
    try:
        load_jobs()
    except Exception as e:
        pytest.fail(e.message)
