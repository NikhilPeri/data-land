import pytest

import os
import pandas as pd
from datetime import datetime
from dataland.scheduler import Scheduler

@pytest.fixture
def schedule():
    return {
        'job_1': {
            'frequency': 'daily',
            'module': 'test.fixtures.jobs.test_job'
        },
        'job_2': {
            'frequency': 'daily',
            'module': 'test.fixtures.jobs.test_job'
        },
        'job_3': {
            'frequency': 'daily',
            'after': '12:00',
            'before': '20:00',
            'module': 'test.fixtures.jobs.test_job'
        },
        'job_4': {
            'last_run':'daily',
            'after': '17:00',
            'before': '20:00',
            'module': 'test.fixtures.jobs.test_job'
        }
    }


@pytest.fixture
def schedule_history():
    return {
        'job_1': {
            'last_run': '2018-04-20-1625',
            'status': 'SUCCESS',
        },
        'job_2': {
            'last_run': '2018-04-20-1625',
            'status': 'FAILED',
        },
        'job_3': {
            'last_run': '2018-04-19-1400',
            'status': 'SUCCESS',
        },
        'job_4': {
            'last_run': '2018-04-19-1625',
            'status': 'SUCCESS',
        },
    }

class TestScheduler(object):

    @pytest.mark.freeze_time('2018-04-20 16:20:00.012')
    def test_pending_jobs(self, schedule, schedule_history):
        scheduler = Scheduler()

        scheduler.schedule = schedule
        scheduler.history = schedule_history

        assert scheduler._pending_jobs() == { k: schedule[k] for k in ['job_2', 'job_3'] }
