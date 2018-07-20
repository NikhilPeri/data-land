import os
import sys
import yaml
import logging
import importlib

from datetime import timedelta, datetime, time
from dataland.file_utils import lastest_file, timestamped_file

DATETIME_FORMAT = '%Y-%m-%d-%H%M'
FREQUENCY_MAPINGS = {
    '1h':     timedelta(hours=1),
    '4h':     timedelta(hours=4),
    '8h':     timedelta(hours=8),
    '12h':    timedelta(hours=12),
    'daily':  timedelta(days=1),
    'weekly': timedelta(days=7),
}

SUCCESS_STATUS = 'SUCCESS'
FAILURE_STATUS = 'FAILED'

class Job(object):
    def run(self):
        raise NotImplemented

class Scheduler(object):
    def __init__(self, schedule_file='config/schedule.yml', log_dir='logs'):
        self._load_schedule(schedule_file)
        self._load_schedule_history(os.path.join(log_dir, 'history'))
        self._configure_logging(os.path.join(log_dir, 'scheduler'))

    def run(self):
        for name, job in self._pending_jobs().items():
            try:
                module = importlib.import_module(job['module'])
                module.job.run()
            except Exception as e:
                logging.error()

            logging.shutdown()


    def _load_schedule(self, file):
        with open(file, 'r') as schedule:
            self.schedule = yaml.load(schedule)

    def _load_schedule_history(self, history_dir):
        self.history = {}
        for job_name in self.schedule.keys():
            self.history[job_name] = {
                'last_run': '0001-01-01-0000',
                'status': None
            }

        with lastest_file(history_dir, type='yml') as schedule_history:
            history = yaml.load(schedule_history)
            if history != None:
                self.history.update(history)

    def _configure_logging(self, namespace):
        logging.basicConfig(
            format='[%(levelname)s] %(asctime)s.%(msecs)03d | %(message)s',
            datefmt='%Y-%m-%d %I:%M:%-S',
            level=20
        )
        file_stream = logging.StreamHandler(stream=timestamped_file(namespace, type='log', mode='a+'))
        console_stream = logging.StreamHandler(stream=sys.stdout)
        logging.getLogger().addHandler(file_stream)
        logging.getLogger().addHandler(console_stream)

    def _pending_jobs(self):
        jobs = {}
        for name, job in self.schedule.items():
            if job.has_key('after') and datetime.now().time() < datetime.strptime(job['after'], '%H:%M').time():
                continue
            if job.has_key('before') and datetime.now().time() > datetime.strptime(job['before'], '%H:%M').time():
                continue

            next_run = datetime.strptime(self.history[name]['last_run'], DATETIME_FORMAT) + FREQUENCY_MAPINGS[job['frequency']]
            if datetime.now() > next_run or self.history[name]['status'] != SUCCESS_STATUS:
                jobs[name] = job

        return jobs

if __name__ == '__main__':
    Scheduler().run()
