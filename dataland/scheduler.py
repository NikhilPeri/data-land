import logging
import os
import schedule
import yaml
import importlib
import pandas as pd

from datetime import timedelta, datetime, time

DATETIME_FORMAT = '%Y-%m-%d-%H%M'

SUCCESS_STATUS = 'SUCCESS'
FAILURE_STATUS = 'FAILED'

class Job(object):
    def __init__(self, sched=[], operations=[]):
        self.module = self.__module__
        self.operations = operations
        if type(sched) is schedule.Job:
            sched = [sched]
        for s in sched:
            s.do(self.run)

    def run(self):
        try:
            logging.info('Job running {}'.format(self.module))
            for operation in self.operations:
                operation.perform()
            logging.info('Job succedded {}'.format(self.module))
        except Exception as e:
            logging.error('Job failed {}'.format(self.module))
if __name__ == '__main__':
    configure_logging()
    # import each job and set the __module__
    # run the scheduler
